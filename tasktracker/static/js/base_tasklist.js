Date.prototype.getWeek = function() {
    var onejan = new Date(this.getFullYear(),0,1);
    var today = new Date(this.getFullYear(),this.getMonth(),this.getDate());
    var dayOfYear = ((today - onejan + 86400000)/86400000);
    return Math.ceil(dayOfYear/7)
  };

Storage.prototype.setObject = function(key, value) {
    this.setItem(key, JSON.stringify(value));
}

Storage.prototype.getObject = function(key) {
    return JSON.parse(this.getItem(key));
}

var tasklist_settings = {
    type : "Day",
    time : new Date()
}

var old_data = null
var active_task = null;
var active_context = null;

add_template_element = function(list_to_append, task_descr, index) {
    
    let prior_class = "";
    switch(task_descr["priority"])
    {
        case "Low":
            prior_class = "prior_low";
            break;
        case "High":
            prior_class = "prior_high";
            break;  
        default:
            break;                  
    }

    // Get template
    var template1 = $("#list_elem_templ").html();
    // Create a new row from the template
    var list_elem_templ = $(template1);
    // button
    var btn = list_elem_templ.find(".btn");
    if ((task_descr["traking"] !== "Fixed") && (task_descr["traking"] !== "Period"))
    {
        btn.addClass("op_text"); 
        btn.css("pointer-events","none");
    }
    // description
    var media_body = list_elem_templ.find(".media-body");
    media_body.append($("<span/>").addClass("descr" + ' ' + prior_class).text(task_descr["desr"]));
    // tracking
    if (task_descr["traking"] === "Fixed")
    {
        media_body.append($("<span/>").addClass("start_time").text(task_descr["datetime_start"]));
        media_body.append($("<span/>").addClass("end_time").text(task_descr["datetime_end"]));
    }
    else if (task_descr["traking"] === "Period")
    {
        media_body.append($("<span/>").addClass("lost_time").text(task_descr["lost_time"]));
    }
    // checkbox
    list_elem_templ.find(".custom-control-input").attr("id", "defaultCheck" + index);
    list_elem_templ.find(".custom-control-label").attr("for", "defaultCheck" + index);

    if (task_descr['parent_task'] !== undefined && task_descr['parent_task'].length > 0)
    {
        in_list = list_elem_templ.children(".list-group"); //.children(".contain")
        $("<div/>").addClass("break").insertBefore(in_list);
        for (var [i, t] of task_descr['parent_task'].entries())
        {
            add_template_element(in_list, t, index + 'L' + String(i));
        }
    }

    // save task in local storage for update need
    sessionStorage.setItem(task_descr["desr"], JSON.stringify(task_descr))

    list_to_append.append(list_elem_templ);
};

fill_tasks = function (tasks, tasks_url) {
    history.pushState({}, null, tasks_url);
    if (tasks["tasks"] !== undefined)
    {
        console.log(tasks["tasks"]);
        console.log(typeof tasks["tasks"]);
        $("#current_tasklist").empty();
        sessionStorage.clear();
        for (var [index, task] of tasks["tasks"].entries())
        {
            console.log(typeof task);
            var task_obj = JSON.parse(task)
            console.log(task_obj);

            add_template_element($("#current_tasklist"), task_obj, String(index));
        }
    }
};

get_tasks = function (tasks_url) {
    history.pushState({}, null, tasks_url);
    $.ajax({
        type: "GET",
        url: tasks_url,
        success : function(tasks) {
            fill_tasks(tasks, tasks_url)
        }
    });
};

strptime = function(str) {
    let tokens = str.split(" ");
    let date = tokens[0].split("/");
    let time = tokens[1].split(":");
    date = date.map(function(num) { return parseInt(num); });
    time = time.map(function(num) { return parseInt(num); });
    if (tokens[2] === 'PM')
    {
        if (time[0] < 12) 
            time[0] += 12;
    }
    
    dt = new Date(date[2], date[0]-1, date[1], time[0], time[1], 0);

    return dt;
};

strftime = function(time) {
    let str = "";
    let days = Math.floor(time/(1000*60*60*24));
    let hours = Math.floor((time/(1000*60*60)) % 24);
    let minutes = Math.floor((time/(1000*60)) % 60);
    let seconds = Math.floor((time/1000) % 60);
    str = '00:';
    str += '00:';
    str += ((days < 10) ? ('0' + String(days)) : String(days)) + ' ';
    str += ((hours < 10) ? ('0' + String(hours)) : String(hours)) + ':';
    str += ((minutes < 10) ? ('0' + String(minutes)) : String(minutes)) + ':';
    str += ((seconds < 10) ? ('0' + String(seconds)) : String(seconds));

    return str;
};

update_timer = function(context) {
    let start = $(context).parent().find(".media-body .start_time").text();
    start = strptime(start);           
    let end = $(context).parent().find(".media-body .end_time").text();
    end = strptime(end);
    let now = new Date();
    let lost_time = "";
    if (now > start)
    {
        if (now >= end)
            lost_time = '00:00:00 00:00:00';
        else 
        lost_time = strftime(end - now);
    }
    else 
    {
        lost_time = strftime(end - start);
    }

    if ($(context).parent().find(".end_time .lost_time").length === 0)
    {          
        $(context).parent().find(".end_time").append('<span class="lost_time"> (' + lost_time + ') </span>');
    }
    else 
    {
        $(context).parent().find(".end_time .lost_time").html('<span class="lost_time"> (' + lost_time + ') </span>');
    }
};

$(document).on('click', '.list-group-item button', function () {
    if ($(this).hasClass("op_text") === false)
    {
        if ($(this).text() === 'Run')
        {
            $(this).removeClass("btn-success");
            $(this).addClass("btn-danger");
            $(this).text("Stop");
            
            if (active_context !== null)
            {
                $(active_context).removeClass("btn-danger");
                $(active_context).addClass("btn-success");
                $(active_context).text("Run");                
            }

            active_context = this;
            active_task = setInterval(function () {
                update_timer(active_context);
            }, 1000); 
                       
            // $("#current_tasklist").find(".btn").each(function ()
            // {
            //     console.log(this);
            //     if (this !== active_context)
            //     {
            //         $(this).removeClass("btn-danger");
            //         $(this).addClass("btn-success");
            //         $(this).text("Run"); 
            //     }
            // });
        }
        else 
        {
            
            $(this).removeClass("btn-danger");
            $(this).addClass("btn-success");
            $(this).text("Run"); 
            //$(this).parent().find(".end_time .lost_time").remove();    
            clearInterval(active_task);  
            active_task = null;
            active_context = null; 
        }
    }
});

$(document).on('change', '.list-group-item input', function () {
    if($(this).prop('checked'))
    {
        $(this).parent().parent().find(".media-body").addClass("op_text"); 
        $(this).parent().parent().find(".btn").addClass("op_text"); 
        if($(this).parent().parent().find(".btn").text() === "Stop")
        {
            clearInterval(active_task); 
        }        
    }
    else 
    {
        $(this).parent().parent().find(".media-body").removeClass("op_text");
        if($(this).parent().parent().find(".media-body .start_time").text() !== "")
        {
            $(this).parent().parent().find(".btn").removeClass("op_text"); 
        }
        if ($(this).parent().parent().find(".btn"))
        if($(this).parent().parent().find(".btn").text() === "Stop" && active_task !== null)
        {         
            active_task = setInterval(function () {
                update_timer(active_context);
            }, 1000);            
        }
    }
});


//update all dropdowns //todo
$(document).on('click', '.btn-group a ', function () {
//$(".btn-group a ").click(function () {
    let p =  $(this).parent().parent();
    p.find('.btn').text($(this).text());
});


get_period = function (period, time) {
    let url = "/tasklist/"
    switch(period)
    {
        case "Day":
            url += "d";
            url += (time.getDate() < 10) ? ('0' + String(time.getDate())) : String(time.getDate());
            url += (time.getMonth() < 9) ? ('0' + String(time.getMonth() + 1)) : String(time.getMonth() + 1);
            url += (String(time.getFullYear())).substring(2,4) + '/';
            break;
        case "Week":
            url += "w";
            url += (time.getWeek() < 10) ? ('0' + String(time.getWeek())) : String(time.getWeek());
            url += (time.getMonth() < 9) ? ('0' + String(time.getMonth() + 1)) : String(time.getMonth() + 1);
            url += (String(time.getFullYear())).substring(2,4) + '/';
            break;
        case "Month":
            url += "m";
            url += (time.getMonth() < 9) ? ('0' + String(time.getMonth() + 1)) : String(time.getMonth() + 1);
            url += (String(time.getFullYear())).substring(2,4) + '/';
            break;
        case "Year":
            url += "y";
            url += (String(time.getFullYear())).substring(2,4) + '/';
            break;
        case "Global":
            url += "g";
            break;
        case "Free":
            url += "f";
            break;
    }

    console.log(url)
    return url
};

update_tasks = function(settings, query_type) {
    if (query_type == "Next >>")
    {
        switch(settings.type)
        {
            case "Day":
                settings.time.setDate(settings.time.getDate() + 1);
                break;
            case "Week":
                settings.time.setDate(settings.time.getDate() + 7);
                break;
            case "Month":
                settings.time.setMonth(settings.time.getMonth() + 1);
                break;
            case "Year":
                settings.time.setFullYear(settings.time.getFullYear() + 1);
                break;
        }
    }
    else if (query_type == "<< Prev")
    {
        switch(settings.type)
        {
            case "Day":
                settings.time.setDate(settings.time.getDate() - 1);
                break;
            case "Week":
                settings.time.setDate(settings.time.getDate() - 7);
                break;
            case "Month":
                settings.time.setMonth(settings.time.getMonth() - 1);
                break;
            case "Year":
                settings.time.setFullYear(settings.time.getFullYear() - 1);
                break;
        }
    }
    else if (query_type == "Current")
    {
        settings.type = "Day"
        settings.time = new Date()
    }
    else 
    {
        settings.type = query_type;
    }

    console.log(settings.time);
    let date_url = get_period(settings.type, settings.time);
    get_tasks(date_url);
    console.log(date_url);
};

$(document).on('click', '.btn', function () {
    let id = $(this).parent().attr("id");
    if (id == "current_period")
        update_tasks(tasklist_settings, $(this).text())
    });

$(function () {
    $("#datetimepicker2").datetimepicker();
});

$(function () {
    $("#datetimepicker1").datetimepicker();
});

getTaskData = function () {
    let start = $("#datetimeinput1").val();
    if ((start === "") || (start === undefined))
    {
        //start = '07/19/2020 4:15 PM'
        dt = new Date();
        start = ((dt.getMonth() < 9) ? ('0' + String(dt.getMonth() + 1)) : String(dt.getMonth() + 1)) + '/';
        start += ((dt.getDate() < 10) ? ('0' + String(dt.getDate())) : String(dt.getDate())) + '/';
        start += String(dt.getFullYear()) + ' ';
        if (dt.getHours() >= 12)
        {
            if (dt.getHours() > 12)
                start += String(dt.getHours() - 12) + ':';
            else 
                start += String(dt.getHours()) + ':';
            start += (dt.getMinutes() < 10) ? ('0' + String(dt.getMinutes())) : String(dt.getMinutes());
            start += ' PM';
        }
        else 
        {
            start += String(dt.getHours()) + ':';
            start += (dt.getMinutes() < 10) ? ('0' + String(dt.getMinutes())) : String(dt.getMinutes());
            start += ' AM';
        }
    }
      
    let template = {   
        "active_intervals" :            $("#active_days_input2").val(),
        "exclude_selected" :            $("#exclude_selected2").is(':checked'),
        "template_counter" :            $("#repeat_counter_form").val()
    };

    let data = {
        "desr"     :                    $("#exampleFormControlTextarea1").val(),
        "priority" :                    $("#task_priority_dropdown_button").text(),
        "traking"  :                    $("#traking_type_dropdown_button").text(),
        "period"   :                    $("#task_period_dropdown_button").text(),
        "is_habit" :                    $("#is_habit").is(':checked'),
        "datetime_start" :              start,
        "datetime_end" :                $("#datetimeinput2").val(),
        "parent_task" :                 $("#parent_task_input").val(),
        "template_intervals" :          template
    };

    return data;
};

$(document).on('click', '#edit_task_button', function () {
    clearModalWindow();
    $("#create_task_modal").modal('show');
    $("#create_task_modal_save_button").text("Create task");
});

//save changes button
//$("#create_task_modal_save_button").click(function () {
$(document).on('click', '#create_task_modal_save_button', function () {
    let tasks_url = get_period(tasklist_settings.type, tasklist_settings.time);
    let data = getTaskData();

    if ($("#create_task_modal_save_button").text() == "Update task")
    {
        data = JSON.stringify ({
            "type"     :                    "edit",
            "old_data" :                    old_data,
            "data"     :                    data 
        });
    }
    else  
    {
        data = JSON.stringify ({
            "type"     :                    "add",
            "data"     :                    data 
        });
    }

    $.ajax({
        type: "POST",
        url: tasks_url,
        data: data,
        success : function(tasks) {
            fill_tasks(tasks, tasks_url)
            if ($("#create_task_modal_save_button").text() == "Update task")
            {
                $("#create_task_modal").modal('hide');
            }
        },
        dataType: "json"
    });  
});

$(document).ready(function() {
    tasklist_settings.type = "Day"
    tasklist_settings.time = new Date()
    update_tasks(tasklist_settings, "Day")
});

get_description = function(context) {
    
    let data = {
        "desr" : $(context).find(".descr").text(),
        "datetime_start" : tokens[2]
    };

    return data;
};

fillModalWindow = function (entry) {
    $("#exampleFormControlTextarea1").val(entry["desr"]);
    $("#task_priority_dropdown_button").text(entry["priority"]);
    $("#traking_type_dropdown_button").text(entry["traking"]);
    $("#task_period_dropdown_button").text(entry["period"]);
    let state = (entry["is_habit"] === 'true') ? true : false;
    $("#is_habit").attr('checked', state);
    $("#datetimeinput1").val(entry["datetime_start"]);
    $("#datetimeinput2").val(entry["datetime_end"]);
    $("#parent_task_input").val(entry["parent_task"]);
    $("#active_days_input2").val(entry["active_intervals"]);
    state = (entry["exclude_selected"] === 'True') ? true : false;
    $("#exclude_selected2").attr('checked', state);
    $("#repeat_counter_form").val(entry["template_counter"]);
};

function clearModalWindow() {
    $("#exampleFormControlTextarea1").val("");
    $("#task_priority_dropdown_button").text("Medium");
    $("#traking_type_dropdown_button").text("Untracked");
    $("#task_period_dropdown_button").text("Day");
    $("#is_habit").attr('checked', false);
    $("#datetimeinput1").val("");
    $("#datetimeinput2").val("");
    $("#parent_task_input").val("");
    $("#active_days_input2").val("");
    $("#exclude_selected2").attr('checked', false);
    $("#repeat_counter_form").val("");
};

$(function() {
    $("#current_tasklist").contextMenu({
        selector: '.list-group-item', 
        callback: function(key, options) {
            console.log('clicked', key, $(this).text());
            if (key == "delete")
            {
                let tasks_url = get_period(tasklist_settings.type, tasklist_settings.time);
                let descr = $(this).find(".descr").text();
                let task = JSON.parse(sessionStorage.getItem(descr));
                let data = {
                    "desr" : descr,
                    "datetime_start" : task['datetime_start']
                };
                $.ajax({
                    type: "POST",
                    url: tasks_url,
                    data: JSON.stringify ({
                        "type"     :                    "delete",
                        "data"     :                    data 
                    }),
                    success : function(tasks) {
                        fill_tasks(tasks, tasks_url)
                    },
                    dataType: "json"
                });
            }
            else if (key == "edit")
            {
                let descr = $(this).find(".descr").text();
                let task = JSON.parse(sessionStorage.getItem(descr));
                old_data = {
                    "desr" : descr,
                    "datetime_start" : task['datetime_start']
                };
                $("#create_task_modal").modal('show');
                $("#create_task_modal_save_button").text("Update task")
                fillModalWindow(task);              
            }
            else if (key = "add_subtask")
            {
                let descr = $(this).find(".descr").text();
                clearModalWindow();
                $("#parent_task_input").val(descr);
                $("#create_task_modal").modal('show');
                $("#create_task_modal_save_button").text("Create task");
            }
        },
        items: {
            "edit": {name: "Edit", icon: "edit"},
            "delete": {name: "Delete", icon: "delete"},
            'add_subtask': {name: "Add subtask", icon: "add"},
        }
    });

    //$('.list-group-item').on('click', function(e){
    $(document).on('click', '.list-group-item', function () {
        console.log('clicked', this, this.innerText);
        //let check = $.contains($(this), $(".lost_time"))
        // let check = $(this).find(".end_time .lost_time").length > 0
        // if (check === false)
        //     $(this).find(".end_time").append('<span class="lost_time"> (00:00:00 00:00:00) </span>');
        // else 
        //     $(this).find(".end_time .lost_time").remove();
    })    
});

//$("#current_tasklist").on( "click", function( clickE ) {
// $(document).on('click', '.list-group-item', function (clickE) {
//     alert(clickE.offsetX + ' ' + clickE.offsetY);
//     console.log('clicked', this);
//     $(this).contextMenu( { x: clickE.offsetX, y: clickE.offsetY } );
// });

// $.contextMenu({
//     //selector: '.list-group-item', 
//     callback: function(key, options) {
//         var m = "clicked: " + key;
//         window.console && console.log(m) || alert(m); 
//     },
//     items: {
//         "edit": {name: "Edit", icon: "edit"},
//         "cut": {name: "Cut", icon: "cut"},
//         "copy": {name: "Copy", icon: "copy"},
//         "paste": {name: "Paste", icon: "paste"},
//         "delete": {name: "Delete", icon: "delete"},
//         "sep1": "---------",
//         "quit": {name: "Quit", icon: "quit"}
//     }
// });
