function loadMonitorPage()
{
    $('#ajaxloader').show();
    window.location.replace("/Monitor=Latest");
};

function loadCopierPage()
{
    $('#ajaxloader').show();
    window.location.replace("/Copier");
};

function loadLogsPage()
{
    $('#ajaxloader').show();
    window.location.replace("/Logs");
};

function loadTorrentPage(torrentid)
{
    $('#ajaxloader').show();
    window.location.replace("/Torrent=" + torrentid);
};

function loadHomePage()
{
    $('#ajaxloader').show();
    window.location.replace("/");
};


