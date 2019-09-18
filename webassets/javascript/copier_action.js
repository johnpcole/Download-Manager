
// Invoke Copier Action Dialog

function showActionDialog(copyid)
{
    alert('<'+copyid+'>');
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
            populateCopyDialog(data.outcomedetail.filepath, data.outcomedetail.outcomes)
            $('#copierdialog').show();
            $('#ajaxloader').hide();
        }
    });
};



// Re-population of copy dialog following reconfiguration

function populateCopyDialog(filepath, copydata)
{
    var outputtext = '<div>'+ filepath +'</div><table>';
    $.each(copydata, function(index)
    {
        var currentitem = copydata[index];
        outputtext = outputtext + '<tr><td>.</td>';

        $.each(currentitem, function(indextwo)
        {
            var currentsubitem = currentitem[indextwo];
            if (currentsubitem != "") {
                outputtext = outputtext + '<td>' + currentsubitem + '</td>';
            };
        });

        outputtext = outputtext + '<td>.</td></tr>';
    });
    outputtext = outputtext + '</table>'
    rerenderText('dialogcontent', outputtext);
};





// Close torrent copy dialog

function closeActionDialog()
{
    $('#copierdialog').hide();
};



