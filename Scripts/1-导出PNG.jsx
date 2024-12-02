var doc = activeDocument;

var png = new ExportOptionsSaveForWeb();

png.PNG8 = false;
png.transparency = true;
png.interlaced = false;
png.includeProfile = false;
png.format = SaveDocumentType.PNG;

doc.exportDocument(
    File(
        doc.path + "/" + doc.name.replace(".psd", ".png").replace(".psb", ".png")
    ),
    ExportType.SAVEFORWEB,
    png
);