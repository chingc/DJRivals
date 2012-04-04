$(document).ready(function () {
    "use strict";
    $(".accordion").accordion({
        active: false,
        autoHeight: false,
        collapsible: true
    });
    $(".pop").accordion({
        changestart: function (event, ui) {
            if (ui.newHeader.text()) {  // activate only on expand
                var disc = ui.newHeader.text().replace(/[^a-zA-Z0-9]/g, "").toLowerCase(),
                    chart = ui.newHeader.parent().parent().prev().text().toLowerCase();
                $.getJSON("./rankings/pop/disc/" + disc + ".json", function (data) {
                    var dj_table,
                        rival_table,
                        dj_records = [],
                        rival_records = [],
                        rival_no_play = [],
                        rival = ["Pakachu", "cgcgngng", "Dan.", "Absurd", "Serika", "DJJEFF20", "Kiba", "Rydia", "evenflow", "Scar", "BluBombr", "Kyon", "Mariposa", "EPHSHI", "novi", "VOXUP", "Butters", "yyr", "Cindy!"];
                    dj_records.push('<tr><th class="rank">Rank</th><th class="icon">Icon</th><th class="djname">DJ</th><th class="score">Score</th></tr>');
                    rival_records.push('<tr><th class="rank">Rank</th><th class="icon">Icon</th><th class="djname">Rival DJ</th><th class="score">Score</th></tr>');
                    $.each(data.ranking[chart], function (key, value) {
                        var img_url = "http://img3.djmaxcrew.com/icon/djicon/40/",
                            rank = '<td class="rank">' + value[0] + "</td>",
                            djicon = '<td class="icon"><img width="52" height="32" src="' + img_url + value[1] + '" /></td>',
                            djname = '<td class="djname">' + value[2] + "</td>",
                            score = '<td class="score">' + value[3] + "</td>",
                            rival_index = $.inArray(value[2], rival);
                        dj_records.push("<tr>" + rank + djicon + djname + score + "</tr>");
                        if (rival_index > -1) {
                            rival_records.push("<tr>" + rank + djicon + djname + score + "</tr>");
                            rival.splice(rival_index, 1);
                        }
                    });
                    $.each(rival, function (key, value) {
                        rival_no_play.push('<tr><td class="rank">.</td><td class="icon"></td><td class="djname">' + value + '</td><td class="score">0</td></tr>');
                    });
                    dj_table = $("<table/>", { html: dj_records.join("\n") });
                    rival_table = $("<table/>", { html: (rival_records.concat(rival_no_play)).join("\n") });
                    ui.newHeader.next().html('<table><tr><td class="djs"></td><td class="rivals"></td></tr></table>');
                    ui.newHeader.next().find(".djs").html(dj_table);
                    ui.newHeader.next().find(".rivals").html(rival_table);
                });
            }
        }
    });
});
