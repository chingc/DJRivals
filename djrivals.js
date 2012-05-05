// todo: code cleanup
$(document).ready(function () {
    "use strict";
    var loading = false,
        settings = {
            me: [],
            rival: [],
            starcutoff: 270000,
            popcutoff: 270000,
            clubcutoff: 1500000,
            missioncutoff: 5000000,
            starmastercutoff: 3000000,
            popmastercutoff: 40000000,
            clubmastercutoff: 20000000,
            missionmastercutoff: 20000000
        },
        charts = ["nm", "hd", "mx"],
        default_accordion = {
            active: false,
            animated: false,
            autoHeight: false,
            collapsible: true
        },
        prune = function () {
            // remove DJ from #myrival if the same DJ is in #myname
            var new_me = $("#myname").tokenInput("get"),
                new_rival = $("#myrival").tokenInput("get"),
                i,
                ilen;
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
            // compare two DJ lists for equality (order is irrelevant)
            var found,
                i,
                j,
                ilen,
                jlen;
            if (list1.length === 0 && list2.length === 0) {
                found = true;
            } else if (list1.length !== list2.length) {
                found = false;
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
                        break;
                    }
                }
            }
            return found ? true : false;
        },
        ranking_table = function (event, ui) {
            // generate the ranking table if it does not exist
            if (ui.newHeader.next().children("p").length > 0) {  // activate on expand and only if "<p>" is found
                var name,
                    chart,
                    link,
                    cutoff;
                switch (ui.newHeader.text()) {
                case "Star Master":
                    chart = false;
                    link = "./database/master/star.json";
                    cutoff = settings.starmastercutoff;
                    break;
                case "Pop Master":
                    chart = false;
                    link = "./database/master/pop.json";
                    cutoff = settings.popmastercutoff;
                    break;
                case "Club Master":
                    chart = false;
                    link = "./database/master/club.json";
                    cutoff = settings.clubmastercutoff;
                    break;
                case "Mission Master":
                    chart = false;
                    link = "./database/master/mission.json";
                    cutoff = settings.missionmastercutoff;
                    break;
                default:
                    switch (ui.newHeader.parent().parent().prev().text()) {
                    case "Star":
                        name = ui.newHeader.text().replace(/\W/g, "").toLowerCase();
                        chart = false;
                        link = "./database/star/" + name + ".json";
                        cutoff = settings.starcutoff;
                        break;
                    case "Club":
                        name = ui.newHeader.text().replace(/\W/g, "").toLowerCase();
                        chart = false;
                        link = "./database/club/" + name + ".json";
                        cutoff = settings.clubcutoff;
                        break;
                    case "Mission":
                        name = ui.newHeader.text().replace(/\W/g, "").toLowerCase();
                        chart = false;
                        link = "./database/mission/" + name + ".json";
                        cutoff = settings.missioncutoff;
                        break;
                    default:
                        name = ui.newHeader.text().replace(/\W/g, "").toLowerCase();
                        chart = ui.newHeader.parent().parent().prev().text().slice(-2).toLowerCase();
                        link = "./database/pop/" + name + ".json";
                        cutoff = settings.popcutoff;
                    }
                }
                $.ajax({
                    url: link,
                    dataType: "json",
                    cache: false
                }).done(function (data) {
                    var ranking = chart ? data[chart].ranking : data.ranking,
                        dj_records = [],
                        rival_records = [],
                        rival_copy = $.extend(true, [], settings.rival),  // local copy for modification
                        rival_found,
                        i,
                        j,
                        ilen,
                        jlen;
                    dj_records.push("<table><tr><th>Rank</th><th>Icon</th><th>DJ</th><th>Score</th></tr>");
                    rival_records.push("<table><tr><th>Rank</th><th>Icon</th><th>Rival DJ</th><th>Score</th></tr>");
                    for (i = 0, ilen = ranking.length; i < ilen; i += 1) {
                        rival_found = false;
                        for (j = 0, jlen = rival_copy.length; j < jlen; j += 1) {
                            if (rival_copy[j].name === ranking[i][2]) {
                                rival_copy.splice(j, 1);
                                rival_found = true;
                                break;
                            }
                        }
                        if (ranking[i][3] >= cutoff) {
                            dj_records.push("<tr><td>" + ranking[i][0] + '</td><td><img src="./images/icon/' + ranking[i][1] + '" /></td><td>' + ranking[i][2] + "</td><td>" + ranking[i][3] + "</td></tr>");
                        }
                        if (rival_found || (settings.me.length > 0 && settings.me[0].name === ranking[i][2])) {
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
        me_section = function (new_me) {
            // generate the me section only if #myname has changed or on page reload
            if (!dj_list_equal(new_me, settings.me) || loading) {
                if (new_me.length === 0) {
                    $("#me").prev().children("a").text("DJ Empty");
                    $("#me").empty().html("<p>Go to settings to enter your DJ name.</p>");
                } else {
                    $.ajax({
                        url: "./database/dj/" + new_me[0].id + ".json",
                        dataType: "json",
                        cache: false
                    }).done(function (data) {
                        var records = [],
                            i,
                            j,
                            ilen,
                            jlen;
                        records.push('<div class="accordion">');
                        records.push('<h3><a href="#">Star</a></h3><div>');
                        records.push('<table class="tablesorter"><thead><tr><th>Disc</th><th>Rank</th><th>Score</th></tr></thead><tbody>');
                        for (i = 0, ilen = data.star.scores.length; i < ilen; i += 1) {
                            records.push("<tr><td>" + data.star.scores[i][0] + "</td><td>" + data.star.scores[i][1] + "</td><td>" + data.star.scores[i][2] + "</td></tr>");
                        }
                        records.push("</tbody></table></div>");
                        for (i = 0, ilen = charts.length; i < ilen; i += 1) {
                            records.push('<h3><a href="#">Pop: ' + charts[i].toUpperCase() + "</a></h3><div>");
                            records.push('<table class="tablesorter"><thead><tr><th>Disc</th><th>Rank</th><th>Score</th></tr></thead><tbody>');
                            for (j = 0, jlen = data.pop[charts[i]].length; j < jlen; j += 1) {
                                records.push("<tr><td>" + data.pop[charts[i]][j][0] + "</td><td>" + data.pop[charts[i]][j][1] + "</td><td>" + data.pop[charts[i]][j][2] + "</td></tr>");
                            }
                            records.push("</tbody></table></div>");
                        }
                        records.push('<h3><a href="#">Club</a></h3><div>');
                        records.push('<table class="tablesorter"><thead><tr><th>Set</th><th>Rank</th><th>Score</th></tr></thead><tbody>');
                        for (i = 0, ilen = data.club.scores.length; i < ilen; i += 1) {
                            records.push("<tr><td>" + data.club.scores[i][0] + "</td><td>" + data.club.scores[i][1] + "</td><td>" + data.club.scores[i][2] + "</td></tr>");
                        }
                        records.push("</tbody></table></div>");
                        records.push('<h3><a href="#">Mission</a></h3><div>');
                        records.push('<table class="tablesorter"><thead><tr><th>Mission</th><th>Rank</th><th>Score</th></tr></thead><tbody>');
                        for (i = 0, ilen = data.mission.scores.length; i < ilen; i += 1) {
                            records.push("<tr><td>" + data.mission.scores[i][0] + "</td><td>" + data.mission.scores[i][1] + "</td><td>" + data.mission.scores[i][2] + "</td></tr>");
                        }
                        records.push("</tbody></table></div>");
                        records.push('<h3><a href="#">Master</a></h3><div>');
                        records.push('<table class="tablesorter"><thead><tr><th>Mode</th><th>Rank</th><th>Score</th></tr></thead><tbody>');
                        records.push("<tr><td>Star</td><td>" + data.star.master[0] + "</td><td>" + data.star.master[1] + "</td></tr>");
                        records.push("<tr><td>Pop</td><td>" + data.pop.master[0] + "</td><td>" + data.pop.master[1] + "</td></tr>");
                        records.push("<tr><td>Club</td><td>" + data.club.master[0] + "</td><td>" + data.club.master[1] + "</td></tr>");
                        records.push("<tr><td>Mission</td><td>" + data.mission.master[0] + "</td><td>" + data.mission.master[1] + "</td></tr>");
                        records.push("</tbody></table></div>");
                        records.push("</div>");
                        $("#me").prev().children("a").text("DJ " + new_me[0].name);
                        $("#me").empty().html(records.join(""));
                        $("#me .accordion").accordion(default_accordion);
                        $("#me .tablesorter").tablesorter();
                    });
                }
                settings.me = $.extend(true, [], new_me);
            }
        },
        rival_section = function (new_rival) {
            // generate the rival section only if #myrival has changed or on page reload
            if (!dj_list_equal(new_rival, settings.rival) || loading) {
                if (new_rival.length === 0) {
                    $("#rival").empty().html("<p>Go to settings to enter your rivals.</p>");
                } else {
                    $.ajax({
                        url: "./database/dj/" + settings.me[0].id + ".json",
                        dataType: "json",
                        cache: false
                    }).done(function (myscores) {
                        var records = [],
                            name,
                            score1,
                            score2,
                            i,
                            j,
                            k,
                            ilen,
                            jlen,
                            klen;
                        records.push('<div class="accordion">');
                        for (i = 0, ilen = new_rival.length; i < ilen; i += 1) {
                            $.ajax({
                                async: false,
                                url: "./database/dj/" + new_rival[i].id + ".json",
                                dataType: "json",
                                cache: false
                            }).done(function (rivalscores) {
                                records.push('<h3><a href="#">' + new_rival[i].name + "</a></h3><div>");
                                records.push('<div class="accordion">');
                                records.push('<h3><a href="#">Star</a></h3><div>');
                                records.push('<table class="tablesorter"><thead><tr><th>Disc</th><th>Me</th><th>Rival</th><th>Delta</th></tr></thead><tbody>');
                                for (j = 0, jlen = myscores.star.scores.length; j < jlen; j += 1) {
                                    name = myscores.star.scores[j][0];
                                    score1 = myscores.star.scores[j][2];
                                    score2 = rivalscores.star.scores[j][2];
                                    records.push("<tr><td>" + name + "</td><td>" + score1 + "</td><td>" + score2 + "</td><td>" + (score1 - score2) + "</td></tr>");
                                }
                                records.push("</tbody></table></div>");
                                for (j = 0, jlen = charts.length; j < jlen; j += 1) {
                                    records.push('<h3><a href="#">Pop: ' + charts[j].toUpperCase() + "</a></h3><div>");
                                    records.push('<table class="tablesorter"><thead><tr><th>Disc</th><th>Me</th><th>Rival</th><th>Delta</th></tr></thead><tbody>');
                                    for (k = 0, klen = myscores.pop[charts[j]].length; k < klen; k += 1) {
                                        name = myscores.pop[charts[j]][k][0];
                                        score1 = myscores.pop[charts[j]][k][2];
                                        score2 = rivalscores.pop[charts[j]][k][2];
                                        records.push("<tr><td>" + name + "</td><td>" + score1 + "</td><td>" + score2 + "</td><td>" + (score1 - score2) + "</td></tr>");
                                    }
                                    records.push("</tbody></table></div>");
                                }
                                records.push('<h3><a href="#">Club</a></h3><div>');
                                records.push('<table class="tablesorter"><thead><tr><th>Set</th><th>Me</th><th>Rival</th><th>Delta</th></tr></thead><tbody>');
                                for (j = 0, jlen = myscores.club.scores.length; j < jlen; j += 1) {
                                    name = myscores.club.scores[j][0];
                                    score1 = myscores.club.scores[j][2];
                                    score2 = rivalscores.club.scores[j][2];
                                    records.push("<tr><td>" + name + "</td><td>" + score1 + "</td><td>" + score2 + "</td><td>" + (score1 - score2) + "</td></tr>");
                                }
                                records.push("</tbody></table></div>");
                                records.push('<h3><a href="#">Mission</a></h3><div>');
                                records.push('<table class="tablesorter"><thead><tr><th>Mission</th><th>Me</th><th>Rival</th><th>Delta</th></tr></thead><tbody>');
                                for (j = 0, jlen = myscores.mission.scores.length; j < jlen; j += 1) {
                                    name = myscores.mission.scores[j][0];
                                    score1 = myscores.mission.scores[j][2];
                                    score2 = rivalscores.mission.scores[j][2];
                                    records.push("<tr><td>" + name + "</td><td>" + score1 + "</td><td>" + score2 + "</td><td>" + (score1 - score2) + "</td></tr>");
                                }
                                records.push("</tbody></table></div>");
                                records.push('<h3><a href="#">Master</a></h3><div>');
                                records.push('<table class="tablesorter"><thead><tr><th>Mode</th><th>Me</th><th>Rival</th><th>Delta</th></tr></thead><tbody>');
                                score1 = myscores.star.master[1];
                                score2 = rivalscores.star.master[1];
                                records.push("<tr><td>Star</td><td>" + score1 + "</td><td>" + score2 + "</td><td>" + (score1 - score2) + "</td></tr>");
                                score1 = myscores.pop.master[1];
                                score2 = rivalscores.pop.master[1];
                                records.push("<tr><td>Pop</td><td>" + score1 + "</td><td>" + score2 + "</td><td>" + (score1 - score2) + "</td></tr>");
                                score1 = myscores.club.master[1];
                                score2 = rivalscores.club.master[1];
                                records.push("<tr><td>Club</td><td>" + score1 + "</td><td>" + score2 + "</td><td>" + (score1 - score2) + "</td></tr>");
                                score1 = myscores.mission.master[1];
                                score2 = rivalscores.mission.master[1];
                                records.push("<tr><td>Mission</td><td>" + score1 + "</td><td>" + score2 + "</td><td>" + (score1 - score2) + "</td></tr>");
                                records.push("</tbody></table></div>");
                                records.push("</div></div>");
                            });
                        }
                        records.push("</div>");
                        $("#rival").empty().html(records.join(""));
                        $("#rival .accordion").accordion(default_accordion);
                        $("#rival .tablesorter").tablesorter();
                    });
                }
                settings.rival = $.extend(true, [], new_rival);
            }
        },
        save_settings = function () {
            // save current settings
            var new_me = $("#myname").tokenInput("get"),
                new_rival = $("#myrival").tokenInput("get"),
                new_cutoff = [$("#starcutoff").val(), $("#popcutoff").val(), $("#clubcutoff").val(), $("#missioncutoff").val(),
                    $("#starmastercutoff").val(), $("#popmastercutoff").val(), $("#clubmastercutoff").val(), $("#missionmastercutoff").val()],
                expire = new Date(),
                result = false;
            if (new_me.length === 0 && new_rival.length > 0) {
                result = "Please enter your DJ name!";
            }
            if (new_cutoff[0].length === 0 || new_cutoff[0].search(/\D/) > -1 ||
                    new_cutoff[1].length === 0 || new_cutoff[1].search(/\D/) > -1 ||
                    new_cutoff[2].length === 0 || new_cutoff[2].search(/\D/) > -1 ||
                    new_cutoff[3].length === 0 || new_cutoff[3].search(/\D/) > -1 ||
                    new_cutoff[4].length === 0 || new_cutoff[4].search(/\D/) > -1 ||
                    new_cutoff[5].length === 0 || new_cutoff[5].search(/\D/) > -1 ||
                    new_cutoff[6].length === 0 || new_cutoff[6].search(/\D/) > -1 ||
                    new_cutoff[7].length === 0 || new_cutoff[7].search(/\D/) > -1) {
                result = "Invalid cutoff score!";
            }
            if (!result) {
                me_section(new_me);
                rival_section(new_rival);
                settings.starcutoff = parseInt(new_cutoff[0], 10);
                settings.popcutoff = parseInt(new_cutoff[1], 10);
                settings.clubcutoff = parseInt(new_cutoff[2], 10);
                settings.missioncutoff = parseInt(new_cutoff[3], 10);
                settings.starmastercutoff = parseInt(new_cutoff[4], 10);
                settings.popmastercutoff = parseInt(new_cutoff[5], 10);
                settings.clubmastercutoff = parseInt(new_cutoff[6], 10);
                settings.missionmastercutoff = parseInt(new_cutoff[7], 10);
                expire.setDate(expire.getDate() + 365);
                document.cookie = "DJRivals_Settings=" + JSON.stringify(settings) + "; expires=" + expire.toUTCString();
                $("#main > div > table").replaceWith("<p>Loading...</p>");  // tables need to be rebuild due to new settings
                $(".pop > div > table").replaceWith("<p>Loading...</p>");  // tables need to be rebuild due to new settings
                result = "Saved!";
            }
            return result;
        },
        load_settings = function () {
            // load settings from cookies
            var cookie = document.cookie.split(/;\s*/),
                saved,
                i,
                ilen;
            for (i = 0, ilen = cookie.length; i < ilen; i += 1) {
                if (cookie[i].indexOf("DJRivals_Settings") === 0) {
                    saved = JSON.parse(cookie[i].slice(cookie[i].indexOf("=") + 1));
                    for (i in saved) {
                        if (i === "me" || i === "rival") {
                            settings[i] = $.extend(true, [], saved[i]);
                        }
                        else {
                            settings[i] = saved[i];
                        }
                    }
                    break;
                }
            }
        },
        status_message = function (message) {
            $("<span> " + message + "</span>").prependTo("#status").fadeOut(5000, function () { $(this).remove(); });
        };

    // load settings
    loading = true;
    load_settings();
    $("#starcutoff").val(settings.starcutoff);
    $("#popcutoff").val(settings.popcutoff);
    $("#clubcutoff").val(settings.clubcutoff);
    $("#missioncutoff").val(settings.missioncutoff);
    $("#starmastercutoff").val(settings.starmastercutoff);
    $("#popmastercutoff").val(settings.popmastercutoff);
    $("#clubmastercutoff").val(settings.clubmastercutoff);
    $("#missionmastercutoff").val(settings.missionmastercutoff);

    // accordions
    $(".accordion").accordion(default_accordion);
    $("#root").bind("accordionchange", ranking_table);

    // autocomplete fields
    $.ajax({
        url: "./database/dj_index.json",
        dataType: "json",
        cache: false
    }).done(function (data) {
        $("#myname").tokenInput(data, {
            animateDropdown: false,
            hintText: "Type in a DJ name",
            theme: "facebook",
            onAdd: prune,
            prePopulate: (settings.me.length > 0) ? settings.me : null,
            tokenLimit: 1
        });
        $("#myrival").tokenInput(data, {
            animateDropdown: false,
            hintText: "Type in a DJ name",
            theme: "facebook",
            onAdd: prune,
            prePopulate: (settings.rival.length > 0) ? settings.rival : null,
            preventDuplicates: true
        });
        save_settings();
        loading = false;
    }).fail(function () {
        $("#myname").prop("disabled", true);
        $("#myrival").prop("disabled", true);
        $("#starcutoff").prop("disabled", true);
        $("#popcutoff").prop("disabled", true);
        $("#clubcutoff").prop("disabled", true);
        $("#missioncutoff").prop("disabled", true);
        $("#starmastercutoff").prop("disabled", true);
        $("#popmastercutoff").prop("disabled", true);
        $("#clubmastercutoff").prop("disabled", true);
        $("#missionmastercutoff").prop("disabled", true);
        $("#save").prop("disabled", true);
    });

    // themes
    $("#themeswitcher").themeswitcher({
        buttonPreText: "",
        cookieExpires: 365,
        cookieName: "DJRivals_Theme",
        height: 345,
        loadTheme: "UI lightness"
    });

    // save button :V
    $("#save").button().click(function () { status_message(save_settings()); });
});
