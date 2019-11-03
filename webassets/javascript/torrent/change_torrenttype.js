
// Change torrent type

function changeTorrentType(newtype)
{
    if (newtype == "movie") {
        setFieldValue('moviename', '');
        setFieldValue('movieyear', '');
        changeAreasState('unknownonlyfields', "Hide");
        changeAreasState('tvshowonlyfields', "Hide");
        changeAreasState('movieonlyfields', "Show");
        changeButtonState('MakeMovie', "Disable");
        changeButtonState('MakeTVShow', "Enable");
        changeButtonState('MakeUnknown', "Enable");
    } else if (newtype == "tvshow") {
        setFieldValue('tvshowselector', '');
        setFieldValue('tvshowseasonselector', '');
        changeAreasState('unknownonlyfields', "Hide");
        changeAreasState('movieonlyfields', "Hide");
        changeAreasState('tvshowonlyfields', "Show");
        changeButtonState('MakeMovie', "Enable");
        changeButtonState('MakeTVShow', "Disable");
        changeButtonState('MakeUnknown', "Enable");
    } else {
        setFieldValue('moviename', '');
        setFieldValue('tvshowselector', '');
        setFieldValue('movieyear', '');
        setFieldValue('tvshowseasonselector', '');
        changeAreasState('tvshowonlyfields', "Hide");
        changeAreasState('movieonlyfields', "Hide");
        changeAreasState('unknownonlyfields', "Show");
        changeButtonState('MakeMovie', "Enable");
        changeButtonState('MakeTVShow', "Enable");
        changeButtonState('MakeUnknown', "Disable");
    };
};
