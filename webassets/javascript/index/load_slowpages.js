function loadMonitor()
{
    $('#ajaxloader').show();
    window.location.replace("/Monitor=Latest");
};

function loadCopier()
{
    $('#ajaxloader').show();
    window.location.replace("/Copier");
};

function loadLogs()
{
    $('#ajaxloader').show();
    window.location.replace("/Logs");
};

function loadTorrent(torrentid)
{
    $('#ajaxloader').show();
    window.location.replace("/Torrent=" + torrentid);
};



