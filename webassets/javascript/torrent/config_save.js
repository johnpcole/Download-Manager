
// Save torrent configuration

function saveTorrentConfiguration()
{
    var newtype = getNewTorrentType();
    var newinstructions = {};
    if (newtype == 'tvshow') {
        newinstructions = { 'torrenttype' : newtype, 'tvshowname' : getFieldValue("tvshowselector"), 'season' : getFieldValue('tvshowseasonselector'), 'fileinstructions' : getFileInstructions("tvshow") };
    } else if (newtype == 'movie') {
        newinstructions = { 'torrenttype' : newtype, 'moviename' : getFieldValue("moviename"), 'year' : getFieldValue('movieyear'), 'fileinstructions' : getFileInstructions("movie") };
    } else {
        newinstructions = { 'torrenttype' : newtype, 'moviename' : getFieldValue("moviename"), 'fileinstructions' : getUnknownTorrentFileInstructions() };
    };
    updateCopyButton(getImageName('Status'), newtype, getImageName('Copy_Overlay'));
    updateDeleteButton(getImageName('Copy_Overlay'));
    updateTorrentConfig(newinstructions);
};


// Ajax call for all torrent configuration data

function updateTorrentConfig(action)
{
    $.ajax({
        url: 'ReconfigureTorrent',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'torrentid':getCurrentTorrentId(), 'newconfiguration':action}),
        dataType:'json',
        beforeSend: function() {
            $('#ajaxloader').show();
        },
        success: function(data){
            updateTorrentConfigDisplay(data.selectedtorrent);
            displayReadMode();
        },
        complete: function(){
            $('#ajaxloader').hide();
        }
    });
};



// Update the displayed data for configured data

function updateTorrentConfigDisplay(dataitem)
{
    rerenderText("TorrentTitle", dataitem.torrenttitle);
    rerenderImage("TorrentType", "torrenttypes/"+dataitem.torrenttype, 'png');

    var filelist = dataitem.files;
    $.each(filelist, function(index)
    {
        rerenderText("filetitle-"+filelist[index].fileid, filelist[index].filetitle);
        rerenderImage("outcome-"+filelist[index].fileid, "fileactions/"+filelist[index].outcome, 'png');
        var filetypelabel = getImageName("filetype-"+filelist[index].fileid);
        updateFileTileColour("File-"+filelist[index].fileid, filetypelabel, filelist[index].outcome);
    });

    populateCopyDialog(dataitem.copyinfo);
};



// Determine new torrent type

function getNewTorrentType()
{
    if (getButtonState('MakeTVShow') == 'Disabled') {
        var newtype = "tvshow";
    } else if (getButtonState('MakeMovie') == 'Disabled') {
        var newtype = "movie";
    } else {
        var newtype = "unknown";
    };
    return newtype;
};




// Get all File designations

function getFileControlStates()
{
    var fileinstructions = [];
    var areaobjectlist = document.getElementsByClassName('copyonlyfields');
    var areaindex;
    var fileid;
    var filetype;
    var subflag;

    for (areaindex = 0; areaindex < areaobjectlist.length; areaindex++) {
        areaobject = areaobjectlist[areaindex];
        fileid = (areaobject.id).substring(11);
        if (getButtonState('MakeIgnore-'+fileid) == 'Disabled') {
            fileinstructions.push([fileid, "ignore", "no-episode", "no-filetype", "no-subtitle"]);
        } else {
            filetype = getImageName("filetype-"+fileid);
            if (filetype == "subtitle") {
                subflag = getFieldValue("subtitleselector-"+fileid);
            } else {
                subflag = "-";
            };
            fileinstructions.push([fileid, "copy", getFieldValue("episodeselector-"+fileid), filetype, subflag]);
        };
    };
    return fileinstructions;
};

// Get sanitised tvshow & movie file designations

function getFileInstructions(torrenttype)
{
    var rawdata = getFileControlStates();
    var rawlength = rawdata.length;
    var loopindex;
    var currentitem;
    var outcome = {};
    var idval;
    var instructionval;
    for (loopindex = 0; loopindex < rawlength; loopindex++) {
        currentitem = rawdata[loopindex];
        idval = currentitem[0];
        if (torrenttype == "movie") {
            currentitem[2] = "Film";
        };
        if ((currentitem[1] == "copy") && (currentitem[2] != "")) {
            instructionval = currentitem[2];
            if ((currentitem[3] == "subtitle") && (currentitem[4] != "")) {
                instructionval = instructionval + "_" + currentitem[4];
            };
        } else {
            instructionval = "ignore";
        };
        outcome[idval] = instructionval;
    };
    return outcome;
};


// Get sanitised tvshow & movie file designations

function getUnknownTorrentFileInstructions()
{
    var rawdata = getFileControlStates();
    var rawlength = rawdata.length;
    var loopindex;
    var currentitem;
    var outcome = {};
    var idval;
    for (loopindex = 0; loopindex < rawlength; loopindex++) {
        currentitem = rawdata[loopindex];
        idval = currentitem[0];
        instructionval = "ignore";
        outcome[idval] = instructionval;
    };
    return outcome;
};


// Show & Hide Areas

function displayReadMode()
{
    changeAreaClass('Page', 'readview');
};