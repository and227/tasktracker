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

fill_tasks = function (tasks, tasks_url) {
    history.pushState({}, null, tasks_url);
    if (tasks["tasks"] !== undefined)
    {
        console.log(tasks["tasks"]);
        console.log(typeof tasks["tasks"]);
        $("#current_tasklist").empty();
        sessionStorage.clear();
        for (var task in tasks["tasks"])
        {
            console.log(typeof task);
            var task_descr = JSON.parse(tasks["tasks"][task])
            console.log(task_descr);
            // build string for indication
            var task_str = task_descr["desr"] + ' - ' + task_descr["priority"]
            if (task_descr["datetime_start"] !== undefined)
                task_str += ' - ' + task_descr["datetime_start"]
            if (task_descr["datetime_end"] !== undefined)
                task_str += ' - ' + task_descr["datetime_end"]
            if (task_descr["lost_time"] !== undefined)
                task_str += ' - ' + task_descr["lost_time"]
            $("#current_tasklist").append(       
                '<li class="list-group-item d-flex align-items-center">' +
                    '<div class="media-body">'+ task_str + '</div>' + 
                    '<div class="custom-control custom-checkbox pmd-checkbox custom-control-inline">' + 
                        '<input class="custom-control-input" type="checkbox" value="" id="defaultCheck{{forloop.counter0}}" unchecked>' +
                        '<label class="custom-control-label" for="defaultCheck{{forloop.counter0}}">' + 
                        '</label>' + 
                    '</div>' + 
                '</li>'); 
            // save task in local storage for update need
            sessionStorage.setItem(task_descr["desr"], JSON.stringify(task_descr))
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
    $("#create_task_modal").modal('show');
    $("#create_task_modal_save_button").text("Create task")
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
        },
        dataType: "json"
    });  
});

$(document).ready(function() {
    tasklist_settings.type = "Day"
    tasklist_settings.time = new Date()
    update_tasks(tasklist_settings, "Day")
});

parse_task_string = function(str) {
    tokens = str.split(' - ');
    let data = {
        "desr" : tokens[0],
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

$(function() {
    $("#current_tasklist").contextMenu({
        selector: '.list-group-item', 
        callback: function(key, options) {
            console.log('clicked', key, $(this).text());
            if (key == "delete")
            {
                let tasks_url = get_period(tasklist_settings.type, tasklist_settings.time);
                let data = parse_task_string($(this).text());
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
                old_data = parse_task_string($(this).text());
                let entry = sessionStorage.getItem(old_data["desr"]);
                entry = JSON.parse(entry);
                $("#create_task_modal").modal('show');
                $("#create_task_modal_save_button").text("Update task")
                fillModalWindow(entry);              
            }
        },
        items: {
            "edit": {name: "Edit", icon: "edit"},
            "delete": {name: "Delete", icon: "delete"},
        }
    });

    //$('.list-group-item').on('click', function(e){
    $(document).on('click', '.list-group-item', function () {
        console.log('clicked', this, this.innerText);
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
