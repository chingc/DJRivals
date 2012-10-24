$(document).ready(function () {
    "use strict";
    var settings = {
            me: "",
            rivals: []
        },
        ranking_table = function (data) {
            var ranking = data.ranking,
                dj_records = [],
                rival_records = [],
                i,
                ilen;
            dj_records.push("<table><tr><th>Rank</th><th>Icon</th><th>DJ</th><th>Score</th></tr>");
            rival_records.push("<table><tr><th>Rank</th><th>Icon</th><th>Rival DJ</th><th>Score</th></tr>");
            for (i = 0, ilen = ranking.length; i < ilen; i += 1) {
                dj_records.push("<tr><td>" + ranking[i][0] + '</td><td><img src="../images/icon/' + ranking[i][1] + '" /></td><td>' + ranking[i][2] + "</td><td>" + ranking[i][3] + "</td></tr>");
            }
            return '<table><tr><td class="djrank">' + dj_records.join("") + '</table></td><td class="rivalrank">' + rival_records.join("") + "</table></td></tr></table>";
        },
        load_tab = function (event, ui) {
            var chart = ui.newTab.children().text(),
                div = $("#" + chart).children(),
                name = div.first().text().replace(/\W/g, "").toLowerCase();
            if (div.last().text() === "Loading...") {
                $.ajax({
                    cache: false,
                    dataType: "json",
                    url: "../database/" + (chart.length === 2 ? "pop_" + chart : chart).toLowerCase() + "/" + name + ".json"
                }).done(function (data) {
                    div.last().empty().html(ranking_table(data));
                }).fail(function () {
                    alert("message on failure");
                });
            }
        };

    // tabs
    $("#tabs").tabs({
        active: false,
        collapsible: true,
        heightStyle: "content",
        activate: load_tab
    });
});
