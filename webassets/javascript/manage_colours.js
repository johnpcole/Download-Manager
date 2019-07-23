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
    var newclassname = "copystate_" + copystatus;
    changeAreaClass(copyid, newclassname);
};
