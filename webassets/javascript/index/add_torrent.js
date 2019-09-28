function addTorrent()
{
    $('#adddialog').show();
};


// Call for adding torrent

function confirmAdd()
{
    $.ajax({
        url: 'AddTorrent',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'newurl': getFieldValue('newurl')}),
        dataType:'json',
        beforeSend: function() {
            $('#ajaxloader').show();
        },
        success: function(data)
        {
            changeButtonState('Add', 'Disable');
            cancelAdd();
        },
        complete: function(){
            $('#ajaxloader').hide();
        }
    });
};

// Close torrent add dialog

function cancelAdd()
{
    $('#adddialog').hide();
};



