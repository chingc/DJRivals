$(document).ready(function () {
    "use strict";
    var me = "",
        rival = [],
        all_djnames = [],
        default_accordion = {
            active: false,
            animated: false,
            autoHeight: false,
            collapsible: true
        },
        pop_accordion_function = function (event, ui) {
            if (ui.newHeader.next().children("p").length !== 0) {  // activate on expand and only if "<p>" is found
                var disc = ui.newHeader.text().replace(/[^a-zA-Z0-9]/g, "").toLowerCase(),
                    chart = ui.newHeader.parent().parent().prev().text().slice(-2).toLowerCase();
                $.ajax({
                    url: "./database/pop/" + disc + ".json",
                    dataType: "json"
                }).done(function (data) {
                    var dj_records = [],
                        rival_records = [],
                        rival_copy = rival.slice(0);  // local copy for modification
                    rival_copy.push(me);  // i am my own rival
                    dj_records.push("<table><tr><th>Rank</th><th>Icon</th><th>DJ</th><th>Score</th></tr>");
                    rival_records.push("<table><tr><th>Rank</th><th>Icon</th><th>Rival DJ</th><th>Score</th></tr>");
                    $.each(data.ranking[chart], function (index, value) {
                        var rival_index = $.inArray(value[2], rival_copy);
                        dj_records.push("<tr><td>" + value[0] + '</td><td><img src="./images/icon/' + value[1] + '" /></td><td>' + value[2] + "</td><td>" + value[3] + "</td></tr>");
                        if (rival_index > -1) {
                            rival_records.push("<tr><td>" + value[0] + '</td><td><img src="./images/icon/' + value[1] + '" /></td><td>' + value[2] + "</td><td>" + value[3] + "</td></tr>");
                            rival_copy.splice(rival_index, 1);
                        }
                    });
                    $.each(rival_copy, function (index, value) { rival_records.push("<tr><td>.</td><td></td><td>" + value + "</td><td>0</td></tr>"); });
                    dj_records.push("</table>");
                    rival_records.push("</table>");
                    ui.newHeader.next().empty().html('<table><tr><td class="djrank">' + dj_records.join("") + '</td><td class="rivalrank">' + rival_records.join("") + "</td></tr></table>");
                });
            }
        },
        rival_accordion_function = function (event, ui) {
        },
        check_and_save = function () {
            var new_me = $("#myname").val().trim(),
                new_rival = $("#myrival").val().split(/,\s*/),
                invalid_names = [];
            if (new_rival[new_rival.length - 1] === "") {
                new_rival.pop();
            }
            if ($.inArray(new_me, all_djnames) < 0) {
                invalid_names.push(new_me);
            }
            $.each(new_rival, function (index, value) {
                if ($.inArray(value, all_djnames) < 0 || value === new_me) {
                    invalid_names.push(value);
                }
            });
            if (invalid_names.length === 0) {
                if (new_me !== me) {
                    me = new_me;
                    if (me === "") {
                        $("#me").prev().children("a").text("DJ Empty");
                        $("#me").empty().html("<p>Go to settings to enter your DJ name.</p>");
                    } else {
                        $.ajax({
                            url: "./database/dj/" + me + ".json",
                            dataType: "json"
                        }).done(function (data) {
                            var records = [];
                            records.push('<div class="accordion">');
                            $.each(["nm", "hd", "mx", "ex"], function (index, value) {
                                records.push('<h3><a href="#">Pop: ' + value.toUpperCase() + "</a></h3><div>");
                                records.push('<table class="tablesorter"><thead><tr><th>Disc</th><th>Score</th></tr></thead><tbody>');
                                $.each(data.pop[value], function (index, value) { records.push("<tr><td>" + value[0] + "</td><td>" + value[1] + "</td></tr>"); });
                                records.push("</tbody></table></div>");
                            });
                            records.push("</div>");
                            $("#me").prev().children("a").text("DJ " + me);
                            $("#me").empty().html(records.join(""));
                            $("#me .accordion").accordion(default_accordion);
                            $("#me .tablesorter").tablesorter();
                        });
                    }
                }
                if (JSON.stringify(new_rival.sort()) !== JSON.stringify(rival)) {
                    rival = new_rival.slice(0);
                    if (rival.length === 0) {
                        $("#rival").empty().html("<p>Go to settings to enter your rivals.</p>");
                    } else {
                        $.ajax({
                            url: "./database/dj/" + me + ".json",
                            dataType: "json"
                        }).done(function (myscore) {
                            var records = [];
                            records.push('<div class="accordion">');
                            $.each(rival, function (index, rivaldj) {
                                if (rivaldj === me) {
                                    return true;
                                }
                                $.ajax({
                                    async: false,
                                    url: "./database/dj/" + rivaldj + ".json",
                                    dataType: "json"
                                }).done(function (rivalscore) {
                                    records.push('<h3><a href="#">' + rivaldj + "</a></h3><div>");
                                    records.push('<div class="accordion">');
                                    $.each(["nm", "hd", "mx"], function (index, chart) {
                                        var i, max, disc, score1, score2;
                                        records.push('<h3><a href="#">Pop: ' + chart.toUpperCase() + "</a></h3><div>");
                                        records.push('<table class="tablesorter"><thead><tr><th>Disc</th><th>Me</th><th>Rival</th><th>Delta</th></tr></thead><tbody>');
                                        for (i = 0, max = myscore.pop[chart].length; i < max; i += 1) {
                                            disc = myscore.pop[chart][i][0];
                                            score1 = myscore.pop[chart][i][1];
                                            score2 = rivalscore.pop[chart][i][1];
                                            records.push("<tr><td>" + disc + "</td><td>" + score1 + "</td><td>" + score2 + "</td><td>" + (score1 - score2) + "</td></tr>");
                                        }
                                        records.push("</tbody></table></div>");
                                    });
                                    records.push("</div></div>");
                                });
                            });
                            records.push("</div>");
                            $("#rival").empty().html(records.join(""));
                            $("#rival .accordion").accordion(default_accordion);
                            $("#rival .tablesorter").tablesorter();
                        });
                    }
                }
                $("<span> (Saved! not really, not until i use cookies)</span>").prependTo("#status").fadeOut(5000, function () { $(this).remove(); });
            } else if (invalid_names[0] === new_me) {
                $("<span> (Not saved.  No need to put yourself in the rival list.)</span>").prependTo("#status").fadeOut(5000, function () { $(this).remove(); });
            } else {
                $("<span> (Not saved.  Invalid DJ Names: " + invalid_names + ")</span>").prependTo("#status").fadeOut(5000, function () { $(this).remove(); });
            }
        };

    // create the accordions
    $(".accordion").accordion(default_accordion);
    $(".pop").bind("accordionchange", pop_accordion_function);

    // create the autocomplete fields
    $.ajax({
        url: "./database/dj/!__all_djnames__.json",
        dataType: "json"
    }).done(function (data) {
        $("#myname").autocomplete({
            focus: function () { return false; },
            source: data
        });
        $("#myrival").bind("keydown", function (event) {
            if (event.keyCode === $.ui.keyCode.TAB && $(this).data("autocomplete").menu.active) {
                event.preventDefault();
            }
        }).autocomplete({
            delay: 600,
            focus: function () { return false; },
            select: function (event, ui) {
                var terms = this.value.split(/,\s*/);
                terms.pop();
                terms.push(ui.item.value, "");
                this.value = terms.join(", ");
                return false;
            },
            source: function (request, response) { response($.ui.autocomplete.filter(data, request.term.split(/,\s*/).pop())); }
        });
        all_djnames = data.slice(0);
    }).fail(function () {
        $("#save").prop("disabled", true);
        $("#myname").prop("disabled", true);
        $("#myrival").prop("disabled", true);
    });

    // save button :V
    $("#save").click(function () { check_and_save(); });
});
