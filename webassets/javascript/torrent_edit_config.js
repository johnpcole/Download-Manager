// Edit torrent configuration

function editTorrentConfiguration()
{
    getTorrentConfig()
};


// Ajax call to get default edit fields

function getTorrentConfig()
{
    $.ajax({
        url: 'EditTorrent',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'torrentid':getCurrentTorrentId()}),
        dataType:'json',
        beforeSend: function() {
            $('#ajaxloader').show();
        },
        success: function(data){
            updateTorrentConfigFields(data.selectedtorrent, data.listitems);
            displayEditMode();
        },
        complete: function(){
            $('#ajaxloader').hide();
        }
    });
};


// Update the edit fields for configured data

function updateTorrentConfigFields(editinfo, listitems)
{
    changeTorrentType(editinfo.torrenttype);
    setFieldValue('moviename', editinfo.moviename);
    setFieldValue('movieyear', editinfo.movieyear);
    repopulateDropDownList('tvshowselector', listitems.tvshows)
    setDropDownValue('tvshowselector', editinfo.tvshowname);
    updateTVShowSeasonsList(listitems.tvshowseasons, editinfo.tvshowseason);
    var filelist = editinfo.files;
    $.each(filelist, function(index)
    {
        var currentfile = filelist[index]
        changeFileDesignation(currentfile.fileid, currentfile.outcome);
        populateFileDropDownLists(currentfile.filetype, currentfile.fileid, listitems)
        if (currentfile.outcome == "copy") {
            if (editinfo.torrenttype == "tvshow") {
                setDropDownValue('episodeselector-'+currentfile.fileid, currentfile.episodeselector);
            };
            if (currentfile.filetype == "subtitle") {
                setDropDownValue('subtitleselector-'+currentfile.fileid, currentfile.subtitleselector);
            };
        };
    });
};


// Populate the file drop-down lists

function populateFileDropDownLists(filetype, fileindex, listitems)
{
    if (filetype != "none") {
        repopulateDropDownList('episodeselector-'+fileindex, listitems.episodes);
        if (filetype == "subtitle") {
            repopulateDropDownList('subtitleselector-'+fileindex, listitems.subtitles)
        };
    };
};


// Show & Hide Areas

function displayEditMode()
{
    changeAreasState('readonlyfields', 'Hide');
    changeAreasState('editmodefields', 'Show');
    changeAreasState('readmodebuttons', 'Hide');
    changeAreasState('editmodebuttons', 'Show');
};
