// Invoke Torrent File Copy

function copyTorrent()
{
    changeButtonState('CloseCopy',"Enable");
    changeButtonState('ConfirmCopy',"Enable");
    $('#copydialog').show();
    var copycounter = setInterval(function() { updateCopyProgress(); }, 1000);
    interactTorrentCopy(getCurrentTorrentId());
};


// Confirm Copy
function confirmCopy()
{
    changeButtonState('CloseCopy',"Disable");
    changeButtonState('ConfirmCopy',"Disable");
    interactTorrentCopy("!!! CONTINUE EXISTING COPY PROCESS !!!");
};


// Ajax call to get default edit fields

function interactTorrentCopy(torrentid)
{
    $.ajax({
        url: 'CopyTorrent',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'copyinstruction':torrentid}),
        dataType:'json',
        success: function(data){
            if (torrentid != "!!! CONTINUE EXISTING COPY PROCESS !!!") {
                populateCopyDialog(data.copydata);
            } else {
                updateCopyDialog(data.copydata);
            };
            if (data.refreshmode == true) {
                interactTorrentCopy("!!! CONTINUE EXISTING COPY PROCESS !!!");
            } else {
                if (torrentid == "!!! CONTINUE EXISTING COPY PROCESS !!!") {
                    changeButtonState('CloseCopy',"Enable");
                };
            };
        }
    });
};


// Initial population of copy dialog

function populateCopyDialog(copydata)
{
    var outputtext = '';
    $.each(copydata, function(index)
    {
        var currentitem = copydata[index];
        outputtext = outputtext + '<div class="dialogitemleft dialogitem">' + currentitem.description + '</div>';
        outputtext = outputtext + '<div id="copydialog-' + index + '" class="dialogitemright dialogitem">';
        outputtext = outputtext + '&nbsp;<img src="./static/images/copy_' + currentitem.status + '.png" /></div>';
    });
    rerenderText('dialogcontent', outputtext);
};


// Update population of copy dialog

function updateCopyDialog(copydata)
{
    $.each(copydata, function(index)
    {
        var currentitem = copydata[index]
        currentobject = 'copydialog-' + index.toString()
        outputtext = ''
        if (currentitem.status != "queued") {
            if ((currentitem.description == "Connect File Server") || (currentitem.description == "Disconnect File Server")) {
                outputtext = outputtext + '(Attempt ' + currentitem.progress + ")"
            };
        };
        if (currentitem.status == "copying") {
            if ((currentitem.description != "Connect File Server") && (currentitem.description != "Disconnect File Server")) {
                rerenderText('copyprogress', 0);
                rerenderText('copystep', (parseInt(110000000000 / currentitem.progress)).toFixed(0));
                outputtext = outputtext + '(~<span id="progressoutput">0</span>%)'
            };
        };
        outputtext = outputtext + '&nbsp;<img src="./static/images/copy_' + currentitem.status + '.png" />';
        rerenderText(currentobject, outputtext);
    });
};


// Close torrent copy dialog

function updateCopyProgress()
{
    var tileData = document.getElementById('progressoutput');
    if (tileData != null) {
        var currentprogress = parseInt(getText('copyprogress'));
        var progressstep = parseInt(getText('copystep'));
        currentprogress = currentprogress + progressstep;
        if (currentprogress > 10000) { currentprogress = 10000};
        rerenderText('copyprogress', currentprogress);
        tileData.innerHTML = (currentprogress/100).toFixed(0);
    };
};


// Close torrent copy dialog

function closeCopyDialog()
{
    //clearInterval(copycounter);
    $('#copydialog').hide();
};




