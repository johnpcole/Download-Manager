
function generateGraphBlocksAndBars(dataset)
{
    var outcome = ''
    $.each(dataset, function(index)
    {
        var logentry = dataset[index];
        outcome = outcome + '<rect x="' + logentry.x
        outcome = outcome + '" y="' + logentry.y
        outcome = outcome + '" height="' + logentry.h
        outcome = outcome + '" width="' + logentry.w
        outcome = outcome + '"></rect>'
    });
    return outcome
};



function generateGraphLines(dataset)
{
    var outcome = ''
    $.each(dataset, function(index)
    {
        var logentry = dataset[index];
        outcome = outcome + '<line x1="' + logentry.xa
        outcome = outcome + '" y1="' + logentry.ya
        outcome = outcome + '" x2="' + logentry.xb
        outcome = outcome + '" y2="' + logentry.yb
        outcome = outcome + '"></line>'
    });
    return outcome
};



function generateGraphText(dataset, textstyle, textalign)
{
    var outcome = ''
    $.each(dataset, function(index)
    {
        var logentry = dataset[index];
        outcome = outcome + '<text text-anchor="' + textalign
        outcome = outcome + '" class="' + textstyle
        outcome = outcome + '" x="' + logentry.x
        outcome = outcome + '" y="' + logentry.y
        outcome = outcome + '">' + logentry.t
        outcome = outcome + '</text>'
    });
    return outcome
};


function generateGraphID(graphindex, label)
{
    var i = graphindex.toString();
    i = i + "_" + label;
    return i;
};


