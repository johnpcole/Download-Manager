function updateTorrentTileColour(tileid, tiletype, torrentstatus)
{
    var newclassname = tiletype + " torrent_" + torrentstatus;
    changeAreaClass(tileid, newclassname);
};


function updateFileTileColour(tileid, filetype, fileoutcome)
{
    var newclassname = "file_" + filetype + "_" + fileoutcome;
    changeAreaClass(tileid, newclassname);
};


function updateIndexBannerTileColour(networkstatus)
{
    var newclassname = "indexbannertile " + networkstatus;
    changeAreaClass("Banner", newclassname);
};