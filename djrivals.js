$(document).ready(function () {
    "use strict";
    $(".accordion").accordion({
        active: false,
        autoHeight: false,
        collapsible: true
    });
    $(".pop").accordion({
        change: function (event, ui) {
            if (ui.newHeader.next().children("p").text()) {  // activate on expand and only if "<p>Loading...</p>" is found
                var disc = ui.newHeader.text().replace(/[^a-zA-Z0-9]/g, "").toLowerCase(),
                    chart = ui.newHeader.parent().parent().prev().text().toLowerCase();
                $.getJSON("./rankings/pop/disc/" + disc + ".json", function (data) {
                    var dj_records = [],
                        rival_records = [],
                        rival_no_play = [],
                        rival = ["Pakachu", "cgcgngng", "Dan.", "Absurd", "Serika", "DJJEFF20", "Kiba", "Rydia", "evenflow", "Scar", "BluBombr", "Kyon", "Mariposa", "EPHSHI", "novi", "VOXUP", "Butters", "yyr", "Cindy!"];
                    dj_records.push('<tr><th class="rank">Rank</th><th class="djicon">Icon</th><th class="djname">DJ</th><th class="score">Score</th></tr>');
                    rival_records.push('<tr><th class="rank">Rank</th><th class="djicon">Icon</th><th class="djname">Rival DJ</th><th class="score">Score</th></tr>');
                    $.each(data.ranking[chart], function (index, value) {
                        var rank = '<td class="rank">' + value[0] + "</td>",
                            djicon = '<td class="djicon"><img width="52" height="32" src="./images/icon/' + value[1] + '" /></td>',
                            djname = '<td class="djname">' + value[2] + "</td>",
                            score = '<td class="score">' + value[3] + "</td>",
                            rival_index = $.inArray(value[2], rival);
                        dj_records.push("<tr>" + rank + djicon + djname + score + "</tr>");
                        if (rival_index > -1) {
                            rival_records.push("<tr>" + rank + djicon + djname + score + "</tr>");
                            rival.splice(rival_index, 1);
                        }
                    });
                    $.each(rival, function (index, value) {
                        rival_no_play.push('<tr><td class="rank">.</td><td class="djicon"></td><td class="djname">' + value + '</td><td class="score">0</td></tr>');
                    });
                    dj_records = $("<table/>", { html: dj_records.join("") });
                    rival_records = $("<table/>", { html: (rival_records.concat(rival_no_play)).join("") });
                    ui.newHeader.next().html('<table><tr><td class="djs"></td><td class="rivals"></td></tr></table>');
                    ui.newHeader.next().find(".djs").html(dj_records);
                    ui.newHeader.next().find(".rivals").html(rival_records);
                });
            }
        }
    });
});
