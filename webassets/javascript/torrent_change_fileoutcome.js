
// Change file designation

function changeFileDesignation(fileid, newtype)
{
    if (newtype == "ignore") {
        changeAreaState('copyconfig-'+fileid, "Hide");
        changeAreaState('ignoreconfig-'+fileid, "Show");
        changeButtonState('MakeIgnore-'+fileid, "Disable");
        changeButtonState('MakeCopy-'+fileid, "Enable");

    } else {
        changeAreaState('ignoreconfig-'+fileid, "Hide");
        changeAreaState('copyconfig-'+fileid, "Show");
        changeButtonState('MakeCopy-'+fileid, "Disable");
        changeButtonState('MakeIgnore-'+fileid, "Enable");
    };
//updateFileTileColour("File-"+fileid, getImageName("filetype-"+fileid), newtype);
};