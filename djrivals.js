$(document).ready(function () {
    "use strict";
    var settings = {
            me: [],
            rival: []
        },
        make_accordion = function (selector, activate) {
            $(selector).accordion({
                active: activate,
                collapsible: true,
                heightStyle: "content"
            });
        },
        make_tabs = function (selector, callable) {
            $(selector).tabs({
                active: false,
                collapsible: true,
                event: "mouseover",
                heightStyle: "content",
                activate: callable
            });
        },
        make_sorter = function (selector) {
            $(selector).tablesorter({
                sortReset: true,
                sortRestart: true
            });
        },
        key_to_array = function (dj, mode) {
            // extract the mode from a dj database as an array
            return $.map(dj[(mode.length === 2 ? "pop_" + mode : mode).toLowerCase()], function (value, key) {
                return [[key, value[0], value[1]]];
            });
        },
        load_tab = function (event, ui) {
            // load ranking page tab content
            var chart = ui.newTab.children().text(),
                div = $("#" + chart).children(),
                name = div.first().text().replace(/\W/g, ""),
                url;
            if (chart.length === 2) {
                chart = "pop_" + chart;
            }
            url = "./database/" + (name === "Master" ? (name + "/" + chart) : (chart + "/" + name)) + ".json";
            if (div.last().text() === "Loading...") {
                $.ajax({
                    cache: false,
                    dataType: "json",
                    url: url.toLowerCase()
                }).done(function (data) {
                    var players = settings.me.concat(settings.rival),
                        no_play = [],
                        dj_section = [],
                        rival_section = [],
                        exit_on_zero = 10,
                        found,
                        i,
                        ilen;
                    data = data.ranking;
                    no_play = $.map(data, function (element) {
                        return element[2];
                    });
                    no_play = $.map(players, function (token, index) {
                        if ($.inArray(token.name, no_play) < 0) {
                            players.splice(index, 1, false);
                            return token.name;
                        }
                    });
                    players = $.map(players, function (token) {
                        if (token) {
                            return token.name;
                        }
                    });
                    dj_section.push("<table><tr><th>Rank</th><th>Icon</th><th>DJ</th><th>Score</th></tr>");
                    rival_section.push("<table><tr><th>Rank</th><th>Icon</th><th>Rival DJ</th><th>Score</th></tr>");
                    for (i = 0, ilen = data.length; i < ilen; i += 1) {
                        if (players.length < 1) {
                            if (exit_on_zero < 1) {
                                break;
                            }
                            exit_on_zero -= 1;
                        }
                        dj_section.push("<tr><td>" + data[i][0] + '</td><td><img src="./images/icon/' + data[i][1] + '" /></td><td>' + data[i][2] + "</td><td>" + data[i][3] + "</td></tr>");
                        found = $.inArray(data[i][2], players);
                        if (found > -1) {
                            rival_section.push("<tr><td>" + data[i][0] + '</td><td><img src="./images/icon/' + data[i][1] + '" /></td><td>' + data[i][2] + "</td><td>" + data[i][3] + "</td></tr>");
                            players.splice(found, 1);
                        }
                    }
                    for (i = 0, ilen = no_play.length; i < ilen; i += 1) {
                        rival_section.push("<tr><td>-</td><td></td><td>" + no_play[i] + "</td><td>-</td></tr>");
                    }
                    div.last().empty().html('<table><tr><td class="djrank">' + dj_section.join("") + '</table></td><td class="rivalrank">' + rival_section.join("") + "</table></td></tr></table>");
                }).fail(function () {
                    div.last().empty().html("Unable to retrieve data.");
                });
            }
        },
        lamp = function (score) {
            var lamp;
            if (score >= 297000) {
                lamp = "fullcombo";
            } else if (score >= 290000) {
                lamp = "exhardclear";
            } else if (score >= 285000) {
                lamp = "hardclear";
            } else if (score >= 270000) {
                lamp = "normalclear";
            } else if (score > 0) {
                lamp = "easyclear";
            } else {
                lamp = "noplay";
            }
            return '<span class="' + lamp + '">&nbsp;</span> ' + score;
        },
        me_section = function (me) {
            if (me.length === 0) {
                $("#me").empty().html("<p>Go to settings to enter your DJ name.</p>");
            } else {
                $.ajax({
                    cache: false,
                    dataType: "json",
                    url: "./database/dj/" + me[0].id + ".json"
                }).done(function (me) {
                    var tabs = ["Star", "NM", "HD", "MX", "Club", "Mission"],
                        section = [],
                        m,
                        i,
                        ilen,
                        j,
                        jlen;
                    section.push('<div id="me_tabs"><ul>');
                    for (i = 0, ilen = tabs.length; i < ilen; i += 1) {
                        section.push('<li><a href="#' + tabs[i] + '">' + tabs[i] + "</a></li>");
                    }
                    section.push("</ul>");
                    for (i = 0, ilen = tabs.length; i < ilen; i += 1) {
                        section.push('<div id="' + tabs[i] + '"><p><img src="./images/icon/' + me.icon + '" />' + me.name + "</p>");
                        section.push('<table class="tablesorter"><thead><tr><th>Title</th><th>Rank</th><th>Score</th></tr></thead><tbody>');
                        m = key_to_array(me, tabs[i]);
                        for (j = 0, jlen = m.length; j < jlen; j += 1) {
                            section.push("<tr><td>" + m[j][0] + "</td><td>" + m[j][1] + "</td><td>" + (m[j][2] <= 300000 ? lamp(m[j][2]) : m[j][2]) + "</td></tr>");
                        }
                        section.pop();
                        section.push("</tbody></table></div>");
                    }
                    section.push("</div>");
                    $("#me").empty().html(section.join(""));
                    make_tabs("#me_tabs");
                    make_sorter(".tablesorter");
                }).fail(function () {
                    $("#me").empty().html("Unable to retrieve data.");
                });
            }
        },
        rival_section = function (me, rival) {
            if (rival.length === 0) {
                $("#rivals").empty().html("<p>Go to settings to enter your DJ rivals.</p>");
            } else {
                $.ajax({
                    cache: false,
                    dataType: "json",
                    url: "./database/dj/" + me[0].id + ".json"
                }).done(function (me) {
                    var tabs = ["Star", "NM", "HD", "MX", "Club", "Mission"],
                        section = [],
                        overall_stats,
                        i,
                        ilen;
                    section.push('<div id="rivals_accordion">');
                    for (i = 0, ilen = rival.length; i < ilen; i += 1) {
                        overall_stats = [0, 0];
                        section.push("<h3>" + rival[i].name + "</h3>");
                        section.push("<div>");
                        $.ajax({
                            async: false,
                            cache: false,
                            dataType: "json",
                            url: "./database/dj/" + rival[i].id + ".json"
                        }).done(function (rival) {
                            var stats,
                                delta,
                                m,
                                r,
                                j,
                                jlen,
                                k,
                                klen;
                            section.push('<div class="rival_tabs"><ul>');
                            for (j = 0, jlen = tabs.length; j < jlen; j += 1) {
                                section.push('<li><a href="#' + tabs[j] + '">' + tabs[j] + "</a></li>");
                            }
                            section.push("</ul>");
                            for (j = 0, jlen = tabs.length; j < jlen; j += 1) {
                                section.push('<div id="' + tabs[j] + '"><p><img src="./images/icon/' + me.icon + '" /> - vs - <img src="./images/icon/' + rival.icon + '" /></p>');
                                section.push('<table class="tablesorter"><thead><tr><th>Title</th><th>Me</th><th>Rival</th><th>Delta</th></tr></thead><tbody>');
                                m = key_to_array(me, tabs[j]);
                                r = key_to_array(rival, tabs[j]);
                                stats = [0, 0, 0];
                                for (k = 0, klen = m.length; k < klen; k += 1) {
                                    delta = m[k][2] - r[k][2];
                                    if (m[k][2] > 0 && r[k][2] > 0) {
                                        delta > 0 ? stats[0]++ : delta < 0 ? stats[1]++ : stats[2]++;
                                    }
                                    section.push("<tr><td>" + m[k][0] + "</td><td>" + (m[k][2] <= 300000 ? lamp(m[k][2]) : m[k][2]) + "</td><td>" + (r[k][2] <= 300000 ? lamp(r[k][2]) : r[k][2]) + "</td><td>" + delta + "</td></tr>");
                                }
                                section.pop();
                                section.push("</tbody></table><br />");
                                section.push('<table id="stats"><thead><tr><th>Win</th><th>Lose</th><th>Draw</th></tr></thead><tbody>');
                                section.push("<tr><td>" + stats[0] + "</td><td>" + stats[1] + "</td><td>" + stats[2] + "</td></tr>");
                                section.push("</tbody></table></div>");
                                overall_stats[0] += stats[0];
                                overall_stats[1] += stats[1];
                            }
                            section.push("</div>");
                        }).fail(function () {
                            section.push("Unable to retrieve data.");
                        });
                        section.push("</div>");
                        section[$.inArray("<h3>" + rival[i].name + "</h3>", section)] = "<h3>" + rival[i].name + "&nbsp; &nbsp;" + overall_stats[0] + ":" + overall_stats[1] + "</h3>";
                    }
                    section.push("</div>");
                    $("#rivals").empty().html(section.join(""));
                    make_accordion("#rivals_accordion", false);
                    make_tabs(".rival_tabs");
                    make_sorter(".tablesorter");
                }).fail(function () {
                    $("#rivals").empty().html("Unable to retrieve data.");
                });
            }
        },
        prune = {
            // functions to help ensure all field content from settings are unique
            f: function (field) {
                // get all ids from a field as an array of ids
                return $.map(field.tokenInput("get"), function (token) {
                    return token.id;
                });
            },
            g: function (id, array) {
                // check if an id exists in the given array
                return $.inArray(id, array) > -1 ? true : false;
            },
            m: function (token) {
                // remove id from #set_me if it exists in #set_rival
                if (prune.g(token.id, prune.f($("#set_rival")))) {
                    $("#set_me").tokenInput("remove", {id: token.id});
                }
            },
            r: function (token) {
                // remove id from #set_rival if it exists in #set_me
                if (prune.g(token.id, prune.f($("#set_me")))) {
                    $("#set_rival").tokenInput("remove", {id: token.id});
                }
            }
        },
        apply_settings = function () {
            // apply settings and save cookie
            var changed = function (array1, array2) {
                    // compare two token input object arrays for equality (order is irrelevant)
                    var a = $.map(array1, function (token) { return token.id; }).sort(),
                        b = $.map(array2, function (token) { return token.id; }).sort();
                    return JSON.stringify(a) !== JSON.stringify(b);
                },
                me = $("#set_me").tokenInput("get"),
                rival = $("#set_rival").tokenInput("get"),
                expire = new Date(new Date().setDate(new Date().getDate() + 365)).toUTCString(),
                message = "";
            if (changed(me, settings.me) || changed(rival, settings.rival)) {
                if (me.length > 0 || (me.length === 0 && rival.length === 0)) {
                    settings.me = me;
                    settings.rival = rival;
                    document.cookie = "DJRivals_Settings=" + JSON.stringify(settings) + "; expires=" + expire;
                    me_section(settings.me);
                    rival_section(settings.me, settings.rival);
                    message = ":D";
                } else {
                    message = "Please enter your DJ name!";
                }
            }
            return message;
        },
        load_settings = function () {
            // load settings from cookie
            var cookie = document.cookie.split(/;\s*/),
                i,
                ilen;
            for (i = 0, ilen = cookie.length; i < ilen; i += 1) {
                if (cookie[i].indexOf("DJRivals_Settings") === 0) {
                    cookie = JSON.parse(cookie[i].slice(cookie[i].indexOf("=") + 1));
                    settings.me = cookie.me;
                    settings.rival = cookie.rival;
                    break;
                }
            }
            me_section(settings.me);
            rival_section(settings.me, settings.rival);
        },
        set_status = function (message) {
            // display a message to the user
            $("#set_status").empty();
            $("<span>" + message + "</span>").prependTo("#set_status").fadeOut(5000, function () { $(this).remove(); });
        };

    make_tabs("#ranking", load_tab);
    make_accordion("#root");

    // autocomplete fields
    $.ajax({
        cache: false,
        dataType: "json",
        url: "./database/dj_index.json"
    }).done(function (data) {
        $("#set_me").tokenInput(data, {
            hintText: "Type a DJ name",
            theme: "facebook",
            onAdd: prune.m,
            prePopulate: settings.me.length > 0 ? settings.me : null,
            tokenLimit: 1
        });
        $("#set_rival").tokenInput(data, {
            hintText: "Type a DJ name",
            theme: "facebook",
            onAdd: prune.r,
            prePopulate: settings.rival.length > 0 ? settings.rival : null,
            preventDuplicates: true
        });
    }).fail(function () {
        $("#set_me").prop("disabled", true);
        $("#set_rival").prop("disabled", true);
        $("#set_apply").prop("disabled", true);
    });

    // apply button :V
    $("#set_apply").button().click(function () { set_status(apply_settings()); });

    load_settings();
});
