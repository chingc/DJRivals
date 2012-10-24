$(document).ready(function () {
    "use strict";
    var settings = {
            me: "",
            rivals: []
        },
        ranking_table = function (data) {
            var players = $.extend([], settings.rivals).concat(settings.me),
                no_play = [],
                dj_records = [],
                rival_records = [],
                exit_on_zero = 5,
                found,
                i,
                ilen;
            no_play = $.map(data, function (element) {
                return element[2];
            });
            no_play = $.map(players, function (name, index) {
                if ($.inArray(name, no_play) < 0) {
                    players.splice(index, 1, false);
                    return name;
                }
            });
            players = $.map(players, function (name) {
                if (name) {
                    return name;
                }
            });
            dj_records.push("<table><tr><th>Rank</th><th>Icon</th><th>DJ</th><th>Score</th></tr>");
            rival_records.push("<table><tr><th>Rank</th><th>Icon</th><th>Rival DJ</th><th>Score</th></tr>");
            for (i = 0, ilen = data.length; i < ilen; i += 1) {
                dj_records.push("<tr><td>" + data[i][0] + '</td><td><img src="../images/icon/' + data[i][1] + '" /></td><td>' + data[i][2] + "</td><td>" + data[i][3] + "</td></tr>");
                found = $.inArray(data[i][2], players);
                if (found > -1) {
                    rival_records.push("<tr><td>" + data[i][0] + '</td><td><img src="../images/icon/' + data[i][1] + '" /></td><td>' + data[i][2] + "</td><td>" + data[i][3] + "</td></tr>");
                    players.splice(found, 1);
                }
                if (players.length < 1) {
                    if (exit_on_zero < 1) {
                        break;
                    }
                    exit_on_zero -= 1;
                }
            }
            for (i = 0, ilen = no_play.length; i < ilen; i += 1) {
                rival_records.push("<tr><td>-</td><td></td><td>" + no_play[i] + "</td><td>-</td></tr>");
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
                    div.last().empty().html(ranking_table(data.ranking));
                }).fail(function () {
                    div.last().empty().html("Unable to retrieve data.");
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
