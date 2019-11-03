//Sets up the page load

$(document).ready(function ()
{
    $('#ajaxloader').hide();
    switchView();
});



// Ajax call for all torrent data

function switchView()
{
    changeButtonState("SwitchView", "Disable");
    var newview = getNewView()
    $.ajax({
        url: 'MonitorData',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'timespan': newview}),
        dataType:'json',
        success: function(data)
        {
            updateMonitorCharts(data.monitoroutput);
            rerenderText("CurrentView", newview);
            changeButtonState("SwitchView", "Enable");
        }
    });
};


function getNewView()
{
    if (getText("CurrentView") == 'Recent') {
        var newview = 'Latest';
    } else {
        var newview = 'Recent';
    };
    return newview;
};




function updateMonitorCharts(graphs)
{
    $.each(graphs, function(index)
    {
        updateMonitorChart(graphs[index], index);
    });
};


function updateMonitorChart(thisgraph, graphindex)
{
    rerenderText(generateGraphID(graphindex,'brightred'), generateGraphBlocksAndBars(thisgraph.brightred));
    rerenderText(generateGraphID(graphindex,'red'), generateGraphBlocksAndBars(thisgraph.red));
    rerenderText(generateGraphID(graphindex,'orange'), generateGraphBlocksAndBars(thisgraph.orange));
    rerenderText(generateGraphID(graphindex,'amber'), generateGraphBlocksAndBars(thisgraph.amber));
    rerenderText(generateGraphID(graphindex,'yellow'), generateGraphBlocksAndBars(thisgraph.yellow));
    rerenderText(generateGraphID(graphindex,'green'), generateGraphBlocksAndBars(thisgraph.green));
    rerenderText(generateGraphID(graphindex,'blue'), generateGraphBlocksAndBars(thisgraph.blue));
    rerenderText(generateGraphID(graphindex,'tempa'), generateGraphBlocksAndBars(thisgraph.tempa));
    rerenderText(generateGraphID(graphindex,'tempb'), generateGraphBlocksAndBars(thisgraph.tempb));
    rerenderText(generateGraphID(graphindex,'tempc'), generateGraphBlocksAndBars(thisgraph.tempc));
    rerenderText(generateGraphID(graphindex,'tempd'), generateGraphBlocksAndBars(thisgraph.tempd));
    rerenderText(generateGraphID(graphindex,'tempe'), generateGraphBlocksAndBars(thisgraph.tempe));
    rerenderText(generateGraphID(graphindex,'axeslines'), generateGraphLines(thisgraph.axeslines));
    rerenderText(generateGraphID(graphindex,'biglabels'), generateGraphText(thisgraph.biglabels, "graphtext", "middle"));
    rerenderText(generateGraphID(graphindex,'littlelabels'), generateGraphText(thisgraph.littlelabels, "littlegraphtext", "middle"));
    rerenderText(generateGraphID(graphindex,'graphtitles'), generateGraphText(thisgraph.graphtitles, "graphheadings", "start"));
    rerenderText(generateGraphID(graphindex,'graphlegends'), generateGraphText(thisgraph.graphlegends, "graphlegends", "start"));
};


