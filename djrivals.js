$(document).ready(function () {
    "use strict";
    var me = "cgcgngng",
        rivals = ["Pakachu", "cgcgngng", "Dan.", "Absurd", "Serika", "DJJEFF20", "Kiba", "Rydia", "evenflow", "Scar", "BluBombr", "Kyon", "Mariposa", "EPHSHI", "novi", "VOXUP", "Butters", "yyr", "Cindy!"],
        default_accordion = {
            active: false,
            animated: false,
            autoHeight: false,
            collapsible: true
        },
        pop_accordion_function = function (event, ui) {
            if (ui.newHeader.next().children("p").text()) {  // activate on expand and only if "<p>Loading...</p>" is found
                var disc = ui.newHeader.text().replace(/[^a-zA-Z0-9]/g, "").toLowerCase(),
                    chart = ui.newHeader.parent().parent().prev().text().toLowerCase();
                $.ajax({
                    url: "./database/pop/" + disc + ".json",
                    dataType: "json"
                }).done(function (data) {
                    var dj_records = [],
                        rival_records = [],
                        rival_no_play = [],
                        rival = rivals.slice(0);  // make local copy for modification
                    dj_records.push("<tr><th>Rank</th><th>Icon</th><th>DJ</th><th>Score</th></tr>");
                    rival_records.push("<tr><th>Rank</th><th>Icon</th><th>Rival DJ</th><th>Score</th></tr>");
                    $.each(data.ranking[chart], function (index, value) {
                        var rank = "<td>" + value[0] + "</td>",
                            djicon = '<td><img src="./images/icon/' + value[1] + '" /></td>',
                            djname = "<td>" + value[2] + "</td>",
                            score = "<td>" + value[3] + "</td>",
                            rival_index = $.inArray(value[2], rival);
                        dj_records.push("<tr>" + rank + djicon + djname + score + "</tr>");
                        if (rival_index > -1) {
                            rival_records.push("<tr>" + rank + djicon + djname + score + "</tr>");
                            rival.splice(rival_index, 1);
                        }
                    });
                    $.each(rival, function (index, value) {
                        rival_no_play.push("<tr><td>.</td><td></td><td>" + value + "</td><td>0</td></tr>");
                    });
                    dj_records = $("<table>", { html: dj_records.join("") });
                    rival_records = $("<table>", { html: (rival_records.concat(rival_no_play)).join("") });
                    ui.newHeader.next().html('<table><tr><td class="djs"></td><td class="rivals"></td></tr></table>');
                    ui.newHeader.next().find(".djs").html(dj_records);
                    ui.newHeader.next().find(".rivals").html(rival_records);
                });
            }
        },
        button_function = function () {
            $.ajax({
                url: "./database/dj_html/" + me + ".html",
                dataType: "html"
            }).done(function (data) {
                $(".me").html(data);
                $(".me").find(".accordion").accordion(default_accordion);
            });
        };
    $(".accordion").accordion(default_accordion);
    $(".pop").bind("accordionchange", pop_accordion_function);
    $("button").click(button_function);
});
