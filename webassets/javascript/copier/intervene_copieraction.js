
// Invoke Copier Action Intervention

function processCopierAction(desiredoutcome)
{
    var copyid = getText("currentlydetailedcopyid");
    $.ajax({
        url: 'PerformCopyIntervention',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'copyid':copyid, 'intervention':desiredoutcome}),
        dataType:'json',
        beforeSend: function() {
            $('#ajaxloader').show();
        },
        success: function(data){
            updateAllCopierTiles(data.copyactions);
            $('#copierdialog').hide();
            $('#ajaxloader').hide();
        }
    });
};


function abandonCopy()
{
    processCopierAction("Abandon");
};

function forceCopy()
{
    processCopierAction("Overwrite");
};

function retryCopy()
{
    processCopierAction("Retry");
};


