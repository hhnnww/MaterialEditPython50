app.bringToFront();

// 开始操作
var selLayers = getSelectedLayersIdx();
var selIdxNames = [];
for (var s in selLayers) {
    selIdxNames.push([
        [Number(selLayers[s])],
        [getLayerNameByIndex(Number(selLayers[s]))]
    ]);
}


selectAllLayers();
var allLayers = getSelectedLayersIdx();
var allIdxNames = [];
for (var n in allLayers) {
    allIdxNames.push([
        [Number(allLayers[n])],
        [getLayerNameByIndex(Number(allLayers[n]))]
    ]);
}

var lList = allIdxNames;
var reg = /\(.*?\)/
var reg2 = /\..*/
for (var z in lList) {
    putLayerNameByIndex(Number(lList[z][0]), activeDocument.name.replace(reg2, '').replace(reg, '') + ' - ' + lList[z][0].toString());
}



function selectLayerByIndex(index, add) {
    add = (add == undefined) ? add = false : add;
    var ref = new ActionReference();
    ref.putIndex(charIDToTypeID("Lyr "), index);
    var desc = new ActionDescriptor();
    desc.putReference(charIDToTypeID("null"), ref);
    if (add) desc.putEnumerated(stringIDToTypeID("selectionModifier"), stringIDToTypeID("selectionModifierType"), stringIDToTypeID("addToSelection"));
    desc.putBoolean(charIDToTypeID("MkVs"), false);
    try {
        executeAction(charIDToTypeID("slct"), desc, DialogModes.NO);
    } catch (e) {}
};

function getLayerNameByIndex(idx) {
    var ref = new ActionReference();
    ref.putProperty(charIDToTypeID("Prpr"), charIDToTypeID("Nm  "));
    ref.putIndex(charIDToTypeID("Lyr "), idx);
    return executeActionGet(ref).getString(charIDToTypeID("Nm  "));
};

function selectAllLayers() {
    var desc29 = new ActionDescriptor();
    var ref23 = new ActionReference();
    ref23.putEnumerated(charIDToTypeID('Lyr '), charIDToTypeID('Ordn'), charIDToTypeID('Trgt'));
    desc29.putReference(charIDToTypeID('null'), ref23);
    executeAction(stringIDToTypeID('selectAllLayers'), desc29, DialogModes.NO);
};

function getSelectedLayersIdx() {
    var selectedLayers = new Array;
    var ref = new ActionReference();
    ref.putEnumerated(charIDToTypeID("Dcmn"), charIDToTypeID("Ordn"), charIDToTypeID("Trgt"));
    var desc = executeActionGet(ref);
    if (desc.hasKey(stringIDToTypeID('targetLayers'))) {
        desc = desc.getList(stringIDToTypeID('targetLayers'));
        var c = desc.count
        var selectedLayers = new Array();
        for (var i = 0; i < c; i++) {
            try {
                activeDocument.backgroundLayer;
                selectedLayers.push(desc.getReference(i).getIndex());
            } catch (e) {
                selectedLayers.push(desc.getReference(i).getIndex() + 1);
            }
        }
    } else {
        var ref = new ActionReference();
        ref.putProperty(charIDToTypeID("Prpr"), charIDToTypeID("ItmI"));
        ref.putEnumerated(charIDToTypeID("Lyr "), charIDToTypeID("Ordn"), charIDToTypeID("Trgt"));
        try {
            activeDocument.backgroundLayer;
            selectedLayers.push(executeActionGet(ref).getInteger(charIDToTypeID("ItmI")) - 1);
        } catch (e) {
            selectedLayers.push(executeActionGet(ref).getInteger(charIDToTypeID("ItmI")));
        }
        var vis = app.activeDocument.activeLayer.visible;
        if (vis == true) app.activeDocument.activeLayer.visible = false;
        var desc9 = new ActionDescriptor();
        var list9 = new ActionList();
        var ref9 = new ActionReference();
        ref9.putEnumerated(charIDToTypeID('Lyr '), charIDToTypeID('Ordn'), charIDToTypeID('Trgt'));
        list9.putReference(ref9);
        desc9.putList(charIDToTypeID('null'), list9);
        executeAction(charIDToTypeID('Shw '), desc9, DialogModes.NO);
        if (app.activeDocument.activeLayer.visible == false) selectedLayers.shift();
        app.activeDocument.activeLayer.visible = vis;
    }
    return selectedLayers;
};

function snapShot() {
    var desc9 = new ActionDescriptor();
    var ref5 = new ActionReference();
    ref5.putClass(charIDToTypeID('SnpS'));
    desc9.putReference(charIDToTypeID('null'), ref5);
    var ref6 = new ActionReference();
    ref6.putProperty(charIDToTypeID('HstS'), charIDToTypeID('CrnH'));
    desc9.putReference(charIDToTypeID('From'), ref6);
    desc9.putEnumerated(charIDToTypeID('Usng'), charIDToTypeID('HstS'), charIDToTypeID('FllD'));
    executeAction(charIDToTypeID('Mk  '), desc9, DialogModes.NO);
};

function putLayerNameByIndex(idx, name) {
    if (idx == 0) return;
    var desc = new ActionDescriptor();
    var ref = new ActionReference();
    ref.putIndex(charIDToTypeID('Lyr '), idx);
    desc.putReference(charIDToTypeID('null'), ref);
    desc.putBoolean(charIDToTypeID("MkVs"), false);
    var nameDesc = new ActionDescriptor();
    nameDesc.putString(charIDToTypeID('Nm  '), name);
    desc.putObject(charIDToTypeID('T   '), charIDToTypeID('Lyr '), nameDesc);
    executeAction(charIDToTypeID('slct'), desc, DialogModes.NO);
    executeAction(charIDToTypeID('setd'), desc, DialogModes.NO);
};