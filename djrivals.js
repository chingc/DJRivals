$(document).ready(function () {
    "use strict";
    var me = [],
        rival = [],
        charts = ["nm", "hd", "mx"],
        default_accordion = {
            active: false,
            animated: false,
            autoHeight: false,
            collapsible: true
        },
        pop_accordion_function = function (event, ui) {
            // generate the rankings table for the main pop sections
            if (ui.newHeader.next().children("p").length > 0) {  // activate on expand and only if "<p>" is found
                var disc = ui.newHeader.text().replace(/[^a-zA-Z0-9]/g, "").toLowerCase(),
                    chart = ui.newHeader.parent().parent().prev().text().slice(-2).toLowerCase();
                $.ajax({
                    url: "./database/pop/" + disc + ".json",
                    dataType: "json"
                }).done(function (data) {
                    var ranking = data[chart].ranking,
                        dj_records = [],
                        rival_records = [],
                        rival_copy = $.extend(true, [], rival),  // local copy for modification
                        rival_index,
                        i, j, ilen, jlen;
                    dj_records.push("<table><tr><th>Rank</th><th>Icon</th><th>DJ</th><th>Score</th></tr>");
                    rival_records.push("<table><tr><th>Rank</th><th>Icon</th><th>Rival DJ</th><th>Score</th></tr>");
                    for (i = 0, ilen = ranking.length; i < ilen; i += 1) {
                        rival_index = -1;
                        for (j = 0, jlen = rival_copy.length; j < jlen; j += 1) {
                            if (rival_copy[j].name === ranking[i][2]) {
                                rival_index = j;
                                break;
                            }
                        }
                        dj_records.push("<tr><td>" + ranking[i][0] + '</td><td><img src="./images/icon/' + ranking[i][1] + '" /></td><td>' + ranking[i][2] + "</td><td>" + ranking[i][3] + "</td></tr>");
                        if (rival_index > -1) {
                            rival_records.push("<tr><td>" + ranking[i][0] + '</td><td><img src="./images/icon/' + ranking[i][1] + '" /></td><td>' + ranking[i][2] + "</td><td>" + ranking[i][3] + "</td></tr>");
                            rival_copy.splice(rival_index, 1);
                        } else if (me.length > 0 && me[0].name === ranking[i][2]) {
                            rival_records.push("<tr><td>" + ranking[i][0] + '</td><td><img src="./images/icon/' + ranking[i][1] + '" /></td><td>' + ranking[i][2] + "</td><td>" + ranking[i][3] + "</td></tr>");
                        }
                    }
                    for (i = 0, ilen = rival_copy.length; i < ilen; i += 1) {
                        rival_records.push("<tr><td>.</td><td></td><td>" + rival_copy[i].name + "</td><td>0</td></tr>");
                    }
                    ui.newHeader.next().empty().html('<table><tr><td class="djrank">' + dj_records.join("") + '</table></td><td class="rivalrank">' + rival_records.join("") + "</table></td></tr></table>");
                });
            }
        },
        prune = function () {
            // remove DJ from #myrival if the same DJ is in #myname
            var new_me = $("#myname").tokenInput("get"),
                new_rival = $("#myrival").tokenInput("get"),
                i, ilen;
            if (new_me.length > 0 && new_rival.length > 0) {
                for (i = 0, ilen = new_rival.length; i < ilen; i += 1) {
                    if (new_rival[i].name === new_me[0].name) {
                        $("#myrival").tokenInput("remove", {name: new_me[0].name});
                        break;
                    }
                }
            }
        },
        dj_list_equal = function (list1, list2) {
            // compare two DJ lists for equality
            var i, j, ilen, jlen, found;
            if (list1.length === 0 && list2.length === 0) {
                return true;
            } else if (list1.length !== list2.length) {
                return false;
            } else {
                for (i = 0, ilen = list1.length; i < ilen; i += 1) {
                    found = false;
                    for (j = 0, jlen = list2.length; j < jlen; j += 1) {
                        if (list1[i].id === list2[j].id && list1[i].name === list2[j].name) {
                            found = true;
                            break;
                        }
                    }
                    if (!found) {
                        return false;
                    }
                }
                return true;
            }
        },
        me_section = function (new_me) {
            // generate the me section if #myname has changed
            if (!dj_list_equal(new_me, me)) {
                if (new_me.length === 0) {
                    $("#me").prev().children("a").text("DJ Empty");
                    $("#me").empty().html("<p>Go to settings to enter your DJ name.</p>");
                } else {
                    $.ajax({
                        url: "./database/dj/" + new_me[0].id + ".json",
                        dataType: "json"
                    }).done(function (data) {
                        var records = [],
                            i, j, ilen, jlen;
                        records.push('<div class="accordion">');
                        for (i = 0, ilen = charts.length; i < ilen; i += 1) {
                            records.push('<h3><a href="#">Pop: ' + charts[i].toUpperCase() + "</a></h3><div>");
                            records.push('<table class="tablesorter"><thead><tr><th>Disc</th><th>Rank</th><th>Score</th></tr></thead><tbody>');
                            for (j = 0, jlen = data.pop[charts[i]].length; j < jlen; j += 1) {
                                records.push("<tr><td>" + data.pop[charts[i]][j][0] + "</td><td>" + data.pop[charts[i]][j][1] + "</td><td>" + data.pop[charts[i]][j][2] + "</td></tr>");
                            }
                            records.push("</tbody></table></div>");
                        }
                        records.push("</div>");
                        $("#me").prev().children("a").text("DJ " + new_me[0].name);
                        $("#me").empty().html(records.join(""));
                        $("#me .accordion").accordion(default_accordion);
                        $("#me .tablesorter").tablesorter();
                    });
                }
                me = $.extend(true, [], new_me);
            }
        },
        rival_section = function (new_rival) {
            // generate the rival section if #myrival has changed
            if (!dj_list_equal(new_rival, rival)) {
                if (new_rival.length === 0) {
                    $("#rival").empty().html("<p>Go to settings to enter your rivals.</p>");
                } else {
                    $.ajax({
                        url: "./database/dj/" + me[0].id + ".json",
                        dataType: "json"
                    }).done(function (myscores) {
                        var records = [],
                            i, j, k, ilen, jlen, klen,
                            disc, score1, score2;
                        records.push('<div class="accordion">');
                        for (i = 0, ilen = new_rival.length; i < ilen; i += 1) {
                            $.ajax({
                                async: false,
                                url: "./database/dj/" + new_rival[i].id + ".json",
                                dataType: "json"
                            }).done(function (rivalscores) {
                                records.push('<h3><a href="#">' + new_rival[i].name + "</a></h3><div>");
                                records.push('<div class="accordion">');
                                for (j = 0, jlen = charts.length; j < jlen; j += 1) {
                                    records.push('<h3><a href="#">Pop: ' + charts[j].toUpperCase() + "</a></h3><div>");
                                    records.push('<table class="tablesorter"><thead><tr><th>Disc</th><th>Me</th><th>Rival</th><th>Delta</th></tr></thead><tbody>');
                                    for (k = 0, klen = myscores.pop[charts[j]].length; k < klen; k += 1) {
                                        disc = myscores.pop[charts[j]][k][0];
                                        score1 = myscores.pop[charts[j]][k][1];
                                        score2 = rivalscores.pop[charts[j]][k][1];
                                        records.push("<tr><td>" + disc + "</td><td>" + score1 + "</td><td>" + score2 + "</td><td>" + (score1 - score2) + "</td></tr>");
                                    }
                                    records.push("</tbody></table></div>");
                                }
                                records.push("</div></div>");
                            });
                        }
                        records.push("</div>");
                        $("#rival").empty().html(records.join(""));
                        $("#rival .accordion").accordion(default_accordion);
                        $("#rival .tablesorter").tablesorter();
                    });
                }
                rival = $.extend(true, [], new_rival);
                $(".pop > div > table").replaceWith("<p>Loading...</p>");
            }
        },
        save_settings = function () {
            // save the current settings and generate the me section and rival section
            var new_me = $("#myname").tokenInput("get"),
                new_rival = $("#myrival").tokenInput("get");
            if (new_me.length === 0 && new_rival.length > 0) {
                $("<span> (Please enter your DJ name!)</span>").prependTo("#status").fadeOut(5000, function () { $(this).remove(); });
            } else {
                me_section(new_me);
                rival_section(new_rival);
            }
        },
        save_cookie = function () {
            // save the current settings to cookies
            var expire = new Date();
            expire.setDate(expire.getDate() + 90);
            expire = "; expires=" + expire.toUTCString();
            document.cookie = "DJR_myname=" + JSON.stringify(me) + expire;
            document.cookie = "DJR_myrival=" + JSON.stringify(rival) + expire;
        },
        load_cookie = function (name) {
            // load stored settings from cookies
            var cookie = document.cookie.split(/;\s*/),
                result = [],
                i, ilen;
            for (i = 0, ilen = cookie.length; i < ilen; i += 1) {
                if (cookie[i].indexOf(name) === 0) {
                    result = cookie[i].slice(cookie[i].indexOf("=") + 1);
                }
            }
            return (result.length > 0) ? JSON.parse(result) : null;
        };

    // create accordions
    $(".accordion").accordion(default_accordion);
    $(".pop").bind("accordionchange", pop_accordion_function);

    // create the autocomplete fields
    $.ajax({
        url: "./database/dj_index.json",
        dataType: "json"
    }).done(function (data) {
        $("#myname").tokenInput(data, {
            animateDropdown: false,
            hintText: "Type in a DJ name",
            theme: "facebook",
            onAdd: prune,
            prePopulate: load_cookie("DJR_myname"),
            tokenLimit: 1
        });
        $("#myrival").tokenInput(data, {
            animateDropdown: false,
            hintText: "Type in a DJ name",
            theme: "facebook",
            onAdd: prune,
            prePopulate: load_cookie("DJR_myrival"),
            preventDuplicates: true
        });
        save_settings();
    }).fail(function () {
        $("#save").prop("disabled", true);
        $("#myname").prop("disabled", true);
        $("#myrival").prop("disabled", true);
    });

    // save button :V
    $("#save").click(function () {
        save_settings();
        save_cookie();
        $("<span> (Saved!)</span>").prependTo("#status").fadeOut(5000, function () { $(this).remove(); });
    });
});
