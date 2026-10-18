// Runs in Figma's sandbox. It only *reads* the selection and posts a plain JSON
// snapshot to the UI, which does the conversion (convert.js) and builds the zip.
// Nothing is flattened, outlined or rasterised here, except image fills, which are
// sent as the original image bytes.

figma.showUI(__html__, { width: 440, height: 640 });

var MIXED = figma.mixed;
function plain(v) { return v === MIXED ? undefined : v; }

function snapshot(node, ctx) {
  var o = {
    id: node.id, name: node.name, type: node.type, visible: node.visible,
    x: node.x, y: node.y, width: node.width, height: node.height,
    opacity: node.opacity, rotation: node.rotation, relativeTransform: node.relativeTransform
  };
  // Extra facts the design analysis needs.
  if ('isMask' in node && node.isMask) o.isMask = true;
  if ('blendMode' in node) o.blendMode = node.blendMode;
  if ('dashPattern' in node && node.dashPattern && node.dashPattern.length) o.dashPattern = node.dashPattern;
  if ('fills' in node) {
    o.fills = plain(node.fills) || [];
    o.fills.forEach(function (p) { if (p.type === 'IMAGE' && p.imageHash) ctx.hashes[p.imageHash] = true; });
  }
  if ('strokes' in node) { o.strokes = node.strokes; o.strokeWeight = plain(node.strokeWeight); o.strokeAlign = node.strokeAlign; if (node.strokeWeight === MIXED) o.strokeMixed = true;
    // How the stroke ends and turns, so dashes and corners match (Figma defaults: no cap, miter join).
    if ('strokeCap' in node) o.strokeCap = plain(node.strokeCap);
    if ('strokeJoin' in node) o.strokeJoin = plain(node.strokeJoin);
  }
  if ('effects' in node) o.effects = node.effects;
  if ('cornerRadius' in node) {
    if (node.cornerRadius === MIXED) {
      o.topLeftRadius = node.topLeftRadius; o.topRightRadius = node.topRightRadius;
      o.bottomLeftRadius = node.bottomLeftRadius; o.bottomRightRadius = node.bottomRightRadius;
    } else o.cornerRadius = node.cornerRadius;
  }
  if ('clipsContent' in node) o.clipsContent = node.clipsContent;
  // Auto layout, on the frame itself.
  if ('layoutMode' in node) {
    o.layoutMode = node.layoutMode; o.layoutWrap = node.layoutWrap;
    o.primaryAxisAlignItems = node.primaryAxisAlignItems; o.counterAxisAlignItems = node.counterAxisAlignItems;
    o.itemSpacing = node.itemSpacing; o.counterAxisSpacing = node.counterAxisSpacing;
    o.paddingLeft = node.paddingLeft; o.paddingRight = node.paddingRight;
    o.paddingTop = node.paddingTop; o.paddingBottom = node.paddingBottom;
  }
  // How this node sits inside an auto layout parent.
  if ('layoutSizingHorizontal' in node) { o.layoutSizingHorizontal = node.layoutSizingHorizontal; o.layoutSizingVertical = node.layoutSizingVertical; }
  if ('layoutPositioning' in node) o.layoutPositioning = node.layoutPositioning;
  ['minWidth', 'maxWidth', 'minHeight', 'maxHeight'].forEach(function (k) { if (node[k]) o[k] = node[k]; });
  if (node.type === 'TEXT') {
    o.characters = node.characters;
    if (node.hasMissingFont) o.hasMissingFont = true;
    o.fontName = plain(node.fontName); o.fontSize = plain(node.fontSize);
    o.textAutoResize = node.textAutoResize;
    o.textAlignHorizontal = node.textAlignHorizontal; o.textAlignVertical = node.textAlignVertical;
    // One entry per run of identical styling, so mixed text stays mixed text.
    o.segments = node.getStyledTextSegments(['fontSize', 'fontName', 'letterSpacing', 'lineHeight', 'fills']);
    o.segments.forEach(function (s) { (s.fills || []).forEach(function (p) { if (p.type === 'IMAGE' && p.imageHash) ctx.hashes[p.imageHash] = true; }); });
  }
  if ('vectorPaths' in node) o.vectorPaths = node.vectorPaths;
  if (node.type === 'INSTANCE') ctx.instances.push(node);
  if ('children' in node) o.children = node.children.map(function (c) { return snapshot(c, ctx); });
  return o;
}

function imageExt(b) {
  if (b[0] === 0x89 && b[1] === 0x50) return 'png';
  if (b[0] === 0xFF && b[1] === 0xD8) return 'jpg';
  if (b[0] === 0x47 && b[1] === 0x49) return 'gif';
  if (b[0] === 0x52 && b[1] === 0x49 && b[8] === 0x57) return 'webp';
  return 'png';
}

async function build(sel, wantComponents, forAnalysis) {
  var ctx = { hashes: {}, instances: [] };
  var nodes = sel.map(function (n) { return snapshot(n, ctx); });
  // Detached instances: collect their main components so they can also become component artboards.
  var components = [], seen = {};
  if (wantComponents) {
    for (var i = 0; i < ctx.instances.length; i++) {
      var main = await ctx.instances[i].getMainComponentAsync();
      if (main && !seen[main.id]) { seen[main.id] = true; components.push(snapshot(main, ctx)); }
    }
  }
  var images = {}, bytes = {};
  var hashes = Object.keys(ctx.hashes);
  for (var j = 0; j < hashes.length; j++) {
    var img = figma.getImageByHash(hashes[j]);
    if (!img) continue;
    var data = await img.getBytesAsync();
    images[hashes[j]] = { ext: imageExt(data), size: data.length };
    if (!forAnalysis) bytes[hashes[j]] = data;
  }
  return { nodes: nodes, components: components, images: images, imageBytes: bytes };
}

function selectionInfo() {
  var sel = figma.currentPage.selection;
  return {
    count: sel.length, names: sel.slice(0, 8).map(function (n) { return n.name; }), types: sel.slice(0, 8).map(function (n) { return n.type; }),
    ids: sel.slice(0, 8).map(function (n) { return n.id; }),
    sizes: sel.slice(0, 8).map(function (n) { return [Math.round(n.width), Math.round(n.height)]; }),
    page: figma.currentPage.name, file: figma.root.name
  };
}
function sendSelection() { var i = selectionInfo(); i.type = 'selection'; figma.ui.postMessage(i); }

figma.ui.onmessage = function (msg) {
  if (msg.type === 'loadSettings') {
    Promise.all([figma.clientStorage.getAsync('token'), figma.clientStorage.getAsync('fileLink'), figma.clientStorage.getAsync('opts'), figma.clientStorage.getAsync('links'), figma.clientStorage.getAsync('recents')]).then(function (v) {
      figma.ui.postMessage({ type: 'settings', token: v[0] || '', fileLink: v[1] || '', opts: v[2] || null, links: v[3] || {}, recents: v[4] || [], selection: selectionInfo() });
    });
    return;
  }
  if (msg.type === 'saveSettings') {
    figma.clientStorage.setAsync('token', msg.token); figma.clientStorage.setAsync('fileLink', msg.fileLink); figma.clientStorage.setAsync('opts', msg.opts);
    if (msg.links) figma.clientStorage.setAsync('links', msg.links);
    if (msg.recents) figma.clientStorage.setAsync('recents', msg.recents);
    return;
  }
  if (msg.type === 'convert') {
    var sel = figma.currentPage.selection;
    if (!sel.length) { figma.ui.postMessage({ type: 'error', message: 'Select one or more frames first.' }); return; }
    build(sel, !!msg.components).then(function (snap) {
      snap.type = 'snapshot'; snap.fileName = figma.root.name;
      figma.ui.postMessage(snap);
    }).catch(function (e) { figma.ui.postMessage({ type: 'error', message: 'Could not read the selection: ' + e.message }); });
  }
  if (msg.type === 'analyze') {
    var sel2 = figma.currentPage.selection;
    if (!sel2.length) { figma.ui.postMessage({ type: 'analysisSnapshot', nodes: [], images: {}, components: [] }); return; }
    build(sel2, false, true).then(function (snap) {
      snap.type = 'analysisSnapshot'; figma.ui.postMessage(snap);
    }).catch(function (e) { figma.ui.postMessage({ type: 'error', message: 'Could not analyse the selection: ' + e.message }); });
  }
  if (msg.type === 'sendToClaude') {
    var sel3 = figma.currentPage.selection;
    if (!sel3.length) { figma.ui.postMessage({ type: 'error', message: 'Select one or more frames first.' }); return; }
    (async function () {
      var snap = await build(sel3, true, true);
      // A PNG of each selected frame, scaled so its longest side is at most 1600px, so Claude can see the design.
      var previews = [];
      for (var i = 0; i < sel3.length && i < 6; i++) {
        var n = sel3[i];
        var scale = Math.min(2, 1600 / Math.max(n.width, n.height, 1));
        try {
          var bytes = await n.exportAsync({ format: 'PNG', constraint: { type: 'SCALE', value: scale } });
          previews.push({ id: n.id, name: n.name, bytes: bytes, scale: scale });
        } catch (e) { /* a layer that cannot be exported is simply skipped */ }
      }
      snap.type = 'claudePayload'; snap.previews = previews; snap.fileName = figma.root.name;
      figma.ui.postMessage(snap);
    })().catch(function (e) { figma.ui.postMessage({ type: 'error', message: 'Could not read the selection: ' + e.message }); });
  }
  if (msg.type === 'select') {
    Promise.all((msg.ids || []).map(function (id) { return figma.getNodeByIdAsync(id); })).then(function (nodes) {
      nodes = nodes.filter(Boolean);
      if (nodes.length) { figma.currentPage.selection = nodes; figma.viewport.scrollAndZoomIntoView(nodes); }
    });
  }
  if (msg.type === 'close') figma.closePlugin();
};

// Tell the UI when the selection changes so the analysis tab can refresh itself.
figma.on('selectionchange', sendSelection);
