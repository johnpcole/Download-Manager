function requestActionDetail(copyid)
{
    var currentstatus = getImageName('Icon_'+copyid);
    currentstatus = currentstatus.substr(10);
    if (((currentstatus == "confirm") || (currentstatus == "failed")) || (currentstatus == "succeeded")) {
        prepareCopyDialogButtons(copyid, currentstatus);
        showActionDialog(copyid);
    };
};


// Invoke Copier Action Dialog

function showActionDialog(copyid)
{
    $.ajax({
        url: 'GetCopyActionDetail',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'copyid':copyid}),
        dataType:'json',
        beforeSend: function() {
            $('#ajaxloader').show();
        },
        success: function(data){
            populateCopyDialog(data.outcomedetail.filepath, data.outcomedetail.description, data.outcomedetail.outcomes)
            $('#copierdialog').show();
            $('#ajaxloader').hide();
        }
    });
};



// Re-population of copy dialog following reconfiguration

function populateCopyDialog(filepath, description, copydata)
{
    var outputtext = '<div class="dialogitemfull">'+ filepath +'</div>';
    outputtext = outputtext + '<div class="dialogitemfull wraptext">'+ description +'</div>';
    outputtext = outputtext + '<table class="copierresultstable">';
    $.each(copydata, function(index)
    {
        var currentitem = copydata[index];
        outputtext = outputtext + '<tr><td></td>';

        $.each(currentitem, function(indextwo)
        {
            var currentsubitem = currentitem[indextwo];
            if (currentsubitem != "") {
                outputtext = outputtext + '<td>' + currentsubitem + '</td>';
            };
        });

        outputtext = outputtext + '<td></td></tr>';
    });
    outputtext = outputtext + '</table>'
    rerenderText('dialogcontent', outputtext);
};





// Close torrent copy dialog

function closeActionDialog()
{
    $('#copierdialog').hide();
};



// Determine button states for dialog

function prepareCopyDialogButtons(copyid, currentstatus)
{
    if ((currentstatus == "confirm") || (currentstatus == "failed")) {
        changeButtonState("AbandonCopy", "Enable");
        changeButtonState("AbandonCopy", "Show");

        if (currentstatus == "confirm") {
            changeButtonState("RetryCopy", "Hide");
            changeButtonState("ConfirmOverwrite", "Show");
        } else {
            changeButtonState("RetryCopy", "Show");
            changeButtonState("ConfirmOverwrite", "Hide");
        };

    } else {
        changeButtonState("AbandonCopy", "Hide");
        changeButtonState("RetryCopy", "Hide");
        changeButtonState("ConfirmOverwrite", "Hide");
    };

    var canattemptagainclass = getAreaClass("TorrentLink_"+copyid)
    if (canattemptagainclass == "strikethrough") {
        changeButtonState("RetryCopy", "Disable");
        changeButtonState("ConfirmOverwrite", "Disable");
    } else {
        changeButtonState("RetryCopy", "Enable");
        changeButtonState("ConfirmOverwrite", "Enable");
    };

};


