#!/usr/bin/env python3
"""Bake auto layout into absolute positions.

usage: flatten_layout.py <scene.rml in> <scene.rml out>

Some runtimes (Webflow's Rive element, for one) lay out nested flex boxes differently and lose their content.
This turns every child that sits in a flex flow into an absolutely placed, fixed-size child at the position the
flow would give it, so the picture no longer depends on the runtime's layout engine.

What it handles: row/column, the nine alignments, gaps, paddings, fixed/fill/hug (the size Figma gave each box is
already on the element). A box that holds text is left as it is, since text sits inside its box by its own rules.
"""
import re, sys
import xml.etree.ElementTree as ET


def fnum(v, d=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return d


def num(v):
    s = ('%.4f' % v).rstrip('0').rstrip('.')
    return s if s not in ('', '-0') else '0'


def style_of(el):
    for c in el:
        if c.tag == 'LayoutComponentStyle':
            return c
    return None


def is_absolute(el):
    st = style_of(el)
    return st is not None and st.get('positionTypeValue') == 'absolute'


def part_of(el):
    for c in el:
        if c.tag == 'LayoutParticipant':
            return c
    return None


def shape_size(shape, inner_w, inner_h):
    """size a shape asks for inside a flow: its participant (fill = the container's inner size), else its path"""
    lp = part_of(shape)
    w = fnum(lp.get('width'), -1) if lp is not None else -1
    h = fnum(lp.get('height'), -1) if lp is not None else -1
    if lp is not None and w < 0 and lp.get('layoutWidthScaleType') == 'fill':
        w = inner_w
    if lp is not None and h < 0 and lp.get('layoutHeightScaleType') == 'fill':
        h = inner_h
    for c in shape:
        if c.tag in ('Rectangle', 'Ellipse'):
            w = w if w >= 0 else fnum(c.get('width'))
            h = h if h >= 0 else fnum(c.get('height'))
    return max(w, 0.0), max(h, 0.0)


def flow_children(container):
    """(element, kind) in document order; kind is 'layout' or 'shape'. Skips absolute ones."""
    out = []
    for c in container:
        if c.tag == 'LayoutComponent' and not is_absolute(c):
            out.append((c, 'layout'))
        elif c.tag in ('Shape', 'Text') and part_of(c) is not None:
            out.append((c, c.tag.lower()))
    return out


def holds_text(container):
    for c in container.iter():
        if c is not container and c.tag == 'Text' and part_of(c) is not None:
            return True
    return False


def align_parts(a):
    v = 'top' if a.startswith('top') else 'bottom' if a.startswith('bottom') else 'center'
    h = 'left' if a.endswith('Left') else 'right' if a.endswith('Right') else 'center'
    if a == 'center':
        v = h = 'center'
    if a == 'centerLeft':
        v, h = 'center', 'left'
    if a == 'centerRight':
        v, h = 'center', 'right'
    return v, h


def place(container, stats):
    st = style_of(container)
    if st is None:
        return
    kids = flow_children(container)
    if not kids:
        return
    texts = [el for el, kind in kids if kind == 'text']
    if any(t_.get('sizingValue') == 'fixed' for t_ in texts):      # a text that already has its fixed box stays in the flow as it is
        return
    if texts:
        # texts have no known width: place them only when nothing after them depends on it
        row_ = st.get('flexDirectionValue', 'row') in ('row', 'rowReverse')
        main_ = st.get('layoutAlignmentType', 'topLeft')
        last_ok = kids[-1][1] == 'text' and len(texts) == 1
        sole = len(kids) == 1
        left_main = main_ in ('topLeft', 'centerLeft', 'bottomLeft') if row_ else main_.startswith('top')
        if not ((last_ok and left_main) or (sole and main_ in ('center', 'centerLeft', 'topLeft'))):
            return
    cw, ch = fnum(container.get('width')), fnum(container.get('height'))
    pl, pr = fnum(st.get('paddingLeft')), fnum(st.get('paddingRight'))
    pt, pb = fnum(st.get('paddingTop')), fnum(st.get('paddingBottom'))
    row = st.get('flexDirectionValue', 'row') in ('row', 'rowReverse')
    gap = fnum(st.get('gapHorizontal' if row else 'gapVertical'))
    algn = st.get('layoutAlignmentType', 'topLeft')
    between = algn.startswith('spaceBetween')
    if between:      # items spread along the main axis; the suffix sets the cross-axis alignment
        cross = algn[len('spaceBetween'):]
        v, h = ('top', 'left') if row and cross == 'Start' else ('center', 'left') if row and cross == 'Center' else ('bottom', 'left') if row else ('top', 'left') if cross == 'Start' else ('top', 'center') if cross == 'Center' else ('top', 'right')
    else:
        v, h = align_parts(algn)
    inner_w, inner_h = cw - pl - pr, ch - pt - pb
    sizes = []
    for el, kind in kids:
        if kind == 'layout':
            sizes.append((fnum(el.get('width')), fnum(el.get('height'))))
        elif kind == 'text':
            paint = next((c for c in el if c.tag == 'TextStylePaint'), None)
            sizes.append((0.0, fnum(paint.get('lineHeight') if paint is not None else None, fnum(paint.get('fontSize') if paint is not None else 16))))
        else:
            sizes.append(shape_size(el, inner_w, inner_h))
    inner_w, inner_h = cw - pl - pr, ch - pt - pb
    # boxes that fill the main axis share what is left; boxes that fill the cross axis take all of it
    grow = [i for i, (el, kind) in enumerate(kids) if kind == 'layout' and style_of(el) is not None and style_of(el).get('layoutWidthScaleType' if row else 'layoutHeightScaleType') == 'fill']
    if grow:
        used = sum((z[0] if row else z[1]) for i, z in enumerate(sizes) if i not in grow) + gap * (len(kids) - 1)
        share = max(0.0, ((inner_w if row else inner_h) - used) / len(grow))
        for i in grow:
            sizes[i] = (share, sizes[i][1]) if row else (sizes[i][0], share)
    for i, (el, kind) in enumerate(kids):
        if kind == 'layout' and style_of(el) is not None and style_of(el).get('layoutHeightScaleType' if row else 'layoutWidthScaleType') == 'fill':
            sizes[i] = (sizes[i][0], inner_h) if row else (inner_w, sizes[i][1])
    for i, (el, kind) in enumerate(kids):
        if kind == 'layout':
            el.set('width', num(sizes[i][0])); el.set('height', num(sizes[i][1]))
    main_total = sum((s[0] if row else s[1]) for s in sizes) + gap * (len(kids) - 1)
    if between and len(kids) > 1:
        gap = max(0.0, ((inner_w if row else inner_h) - sum((z[0] if row else z[1]) for z in sizes)) / (len(kids) - 1))
        main_total = sum((z[0] if row else z[1]) for z in sizes) + gap * (len(kids) - 1)
    main_room = inner_w if row else inner_h
    main_align = h if row else v
    cross_align = v if row else h
    start = {'left': 0, 'top': 0, 'center': (main_room - main_total) / 2, 'right': main_room - main_total, 'bottom': main_room - main_total}[main_align]
    pos = (pl if row else pt) + start
    moved = []
    for (el, kind), (w, hh) in zip(kids, sizes):
        cross_room = inner_h if row else inner_w
        csize = hh if row else w
        co = {'left': 0, 'top': 0, 'center': (cross_room - csize) / 2, 'right': cross_room - csize, 'bottom': cross_room - csize}[cross_align]
        cpos = (pt if row else pl) + co
        left, top = (pos, cpos) if row else (cpos, pos)
        if kind == 'text':
            el.remove(part_of(el))
            if len(kids) == 1 and main_align == 'center':        # a lone, centred text keeps itself centred
                el.set('x', num(pl + inner_w / 2)); el.set('y', num(pt + inner_h / 2)); el.set('originX', '0.5'); el.set('originY', '0.5')
                el.set('alignValue', 'center')
            else:
                el.set('x', num(left)); el.set('y', num(top))
            moved.append(el)
        elif kind == 'layout':
            est = style_of(el)
            est.set('positionTypeValue', 'absolute')
            for k, val in (('positionLeft', left), ('positionTop', top)):
                est.set(k, num(val)); est.set(k + 'UnitsValue', 'points')
            est.set('layoutWidthScaleType', 'fixed'); est.set('layoutHeightScaleType', 'fixed')
        else:
            el.set('x', num(left + w / 2)); el.set('y', num(top + hh / 2))
            el.remove(part_of(el))
            moved.append(el)
            for pth in el:            # a rectangle or ellipse takes the size the flow gave it
                if pth.tag in ('Rectangle', 'Ellipse'):
                    pth.set('width', num(w)); pth.set('height', num(hh))
        stats['placed'] += 1
        pos += (w if row else hh) + gap
    if moved:      # free shapes sit in a Node (as the converter does for icons), or the layout would still stretch them
        at = list(container).index(moved[0])
        wrap = ET.Element('Node', {'name': '%s (Flat)' % container.get('name', 'box')})
        for el in moved:
            container.remove(el)
            wrap.append(el)
        container.insert(at, wrap)


def wrap_loose_shapes(root):
    """Shapes and texts that sit straight under a layout box (no layout participant) are treated as flow items by
    Webflow's runtime and get stretched. Put each run of them in a plain Node, which keeps them free."""
    n = 0
    for box in list(root.iter('LayoutComponent')):
        run = []
        for c in list(box) + [None]:
            if c is not None and c.tag in ('Shape', 'Text') and part_of(c) is None:
                run.append(c); continue
            if run:
                at = list(box).index(run[0])
                node = ET.Element('Node', {'name': '%s (Free)' % (box.get('name') or 'box')})
                for el in run:
                    box.remove(el); node.append(el)
                box.insert(at, node); n += 1; run = []
    return n


def nodes_to_layouts(root):
    """Webflow's Rive runtime (2.35) does not lay out a LayoutComponent that sits inside a plain Node.
    The converter wraps every layout's children in `<Node name='X (Wrapper)'>`; turn each such wrapper into a fixed,
    absolutely placed LayoutComponent the size of its parent, so every box has a layout parent."""
    n = 0
    def walk(el):
        nonlocal n
        for i, c in enumerate(list(el)):
            walk(c)
            if (c.tag == 'Node' and el.tag == 'LayoutComponent' and any(k.tag == 'LayoutComponent' for k in c)
                    and not any(abs(fnum(c.get(a), d)) > 1e-6 for a, d in (('x', 0), ('y', 0), ('rotation', 0))) and fnum(c.get('scaleX'), 1) == 1 and fnum(c.get('scaleY'), 1) == 1):      # (a file pulled from Rive has no names on its nodes)
                w, h = el.get('width', '0'), el.get('height', '0')
                box = ET.Element('LayoutComponent', {'width': w, 'height': h, 'clip': 'false', 'name': c.get('name') or '%s (Box)' % (el.get('name') or 'box')})
                if c.get('id'):
                    box.set('id', c.get('id'))
                st = ET.SubElement(box, 'LayoutComponentStyle', {
                    'layoutWidthScaleType': 'fixed', 'layoutHeightScaleType': 'fixed', 'positionTypeValue': 'absolute',
                    'positionLeft': '0', 'positionLeftUnitsValue': 'points', 'positionTop': '0', 'positionTopUnitsValue': 'points',
                    'name': (c.get('name') or '%s (Box)' % (el.get('name') or 'box')) + ' Style'})
                pst = style_of(el)      # the box takes over the parent's flow settings, because the Node was transparent to them
                if pst is not None:
                    for key, val in pst.attrib.items():
                        if key.startswith(('flex', 'gap', 'padding', 'layoutAlignment')) or key == 'flexWrapValue':
                            st.set(key, val)
                for k in list(c):
                    box.append(k)
                el.remove(c); el.insert(i, box)
                n += 1
    walk(root)
    return n


def fix_lone_text(root):
    """A text that is the only child of a centred fixed box (the 'AI' ball) is measured differently by older runtimes
    and lands off-centre. Give it the box's full width and its own line height, centred, so nothing depends on the measure."""
    n = 0
    for box in root.iter('LayoutComponent'):
        st = style_of(box)
        if st is None or st.get('layoutAlignmentType') != 'center':
            continue
        if fnum(box.get('width')) < 80:      # only the big round 'AI' ball; small pills keep their own measure
            continue
        flow = [c for c in box if (c.tag == 'LayoutComponent' and not is_absolute(c)) or (c.tag == 'Text' and part_of(c) is not None)]
        if len(flow) != 1 or flow[0].tag != 'Text':
            continue
        txt, lp = flow[0], part_of(flow[0])
        if lp.get('layoutWidthScaleType') != 'hug':
            continue
        paint = next((c for c in txt if c.tag == 'TextStylePaint'), None)
        lh = fnum(paint.get('lineHeight') if paint is not None else None, fnum(paint.get('fontSize') if paint is not None else 16))
        w = fnum(box.get('width')) - fnum(st.get('paddingLeft')) - fnum(st.get('paddingRight'))
        lp.set('layoutWidthScaleType', 'fixed'); lp.set('layoutHeightScaleType', 'fixed')
        lp.set('width', num(w)); lp.set('height', num(lh))
        txt.set('sizingValue', 'fixed'); txt.set('alignValue', 'center'); txt.set('verticalAlignValue', 'middle')
        n += 1
    return n


def flatten(text):
    # the file is a fragment with one root element
    root = ET.fromstring(text)
    stats = {'placed': 0}
    nodes_to_layouts(root)
    wrap_loose_shapes(root)
    fix_lone_text(root)
    for el in list(root.iter('LayoutComponent')):      # a list: placing a box adds wrapper nodes, which must not disturb the walk
        place(el, stats)
    out = ET.tostring(root, encoding='unicode')
    return out, stats['placed']


if __name__ == '__main__':
    src = open(sys.argv[1]).read()
    out, n = flatten(src)
    open(sys.argv[2], 'w').write(out)
    print('placed', n, 'children')
