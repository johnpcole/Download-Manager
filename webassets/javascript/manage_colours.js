function updateTorrentTileColour(tileid, tiletype, torrentstatus)
{
    var newclassname = tiletype + " torrent_" + torrentstatus;
    changeAreaClass(tileid, newclassname);
};


function updateFileTileColour(tileid, filetype, fileoutcome)
{
    var newclassname = "contenttile file_" + filetype + "_" + fileoutcome;
    changeAreaClass(tileid, newclassname);
};


function updateBannerTileColour(networkstatus)
{
    var newclassname = "bannertile " + networkstatus;
    changeAreaClass("IndexBanner", newclassname);
};