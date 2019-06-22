function updateTorrentTileColour(tileid, tiletype, torrentstatus)
{
    var newclassname = "tile " + tiletype + " torrent_" + torrentstatus;
    changeAreaClass(tileid, newclassname);
};


function updateFileTileColour(tileid, filetype, fileoutcome)
{
    var newclassname = "tile contenttile file_" + filetype + "_" + fileoutcome;
    changeAreaClass(tileid, newclassname);
};


function updateBannerTileColour(networkstatus)
{
    var newclassname = "tile bannertile " + networkstatus;
    changeAreaClass("IndexBanner", newclassname);
};