function updateTorrentTileColour(tileid, torrentstatus)
{
    var newclassname = "torrent_" + torrentstatus;
    changeAreaClass(tileid, newclassname);
};


function updateFileTileColour(tileid, filetype, fileoutcome)
{
    var newclassname = "file_" + filetype + "_" + fileoutcome;
    changeAreaClass(tileid, newclassname);
};


function updateIndexBannerTileColour(networkstatus)
{
    var newclassname = networkstatus;
    changeAreaClass("IndexBanner", newclassname);
};


function updateCopierTileColour(copyid, copystatus)
{
    var currentclassname = getAreaClass("CopyItem_"+copyid)
    if (currentclassname.substr(4) == "copy") {
        var newclassname = "copystate_" + copystatus;
    } else {
        var newclassname = "scrapestate_" + copystatus;
       };
    changeAreaClass(copyid, newclassname);
};
