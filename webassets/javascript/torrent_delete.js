// Invoke Torrent Delete

function deleteTorrent()
{
    $('#deletedialog').show();
};


// Confirm Delete

function confirmDelete()
{
    $.ajax({
        url: 'DeleteTorrent',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'deleteinstruction':getCurrentTorrentId()}),
        dataType:'json',
        beforeSend: function() {
            $('#ajaxloader').show();
        },
        success: function(data){
            window.location.replace("/");
        }
    });
};



// Close torrent copy dialog

function cancelDelete()
{
    $('#deletedialog').hide();
};



