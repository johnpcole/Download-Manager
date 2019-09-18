
// Invoke Copier Action Dialog

function showActionDialog(copyid)
    alert(copyid);
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
            populateCopyDialog(data.outcomedetail)
            $('#copierdialog').show();
            $('#ajaxloader').hide();
        }
    });
};



// Re-population of copy dialog following reconfiguration

function populateCopyDialog(copydata)
{
    var outputtext = '';
    $.each(copydata, function(index)
    {
        var currentitem = copydata[index];
        outputtext = outputtext + '<div class="dialogitemmax">' + currentitem + '</div>';
    });
    rerenderText('dialogcontent', outputtext);
};





// Close torrent copy dialog

function closeActionDialog()
{
    $('#copierdialog').hide();
};



