Date.prototype.getWeek = function() {
    var onejan = new Date(this.getFullYear(),0,1);
    var today = new Date(this.getFullYear(),this.getMonth(),this.getDate());
    var dayOfYear = ((today - onejan + 86400000)/86400000);
    return Math.ceil(dayOfYear/7)
  };

var tasklist_settings = {
    type : "Day",
    time : new Date()
}

get_tasks = function (tasks_url) {
    history.pushState({}, null, tasks_url);
    $.ajax({
        type: "GET",
        url: tasks_url,
        success : function(tasks) {
            //tasks = data; //JSON.stringify(data)
            console.log("Прибыли данные: " +  tasks);
            console.log(typeof tasks);
            if (tasks["tasks"] !== undefined)
            {
                console.log(tasks["tasks"]);
                console.log(typeof tasks["tasks"]);
                $("#current_tasklist").empty() 
                for (var task in tasks["tasks"])
                {
                    console.log(typeof task);
                    var task_descr = JSON.parse(tasks["tasks"][task])
                    console.log(task_descr);
                    var task_str = task_descr["descriprion"] + ' - ' + task_descr["priority"]
                    if (task_descr["task_begin"] !== undefined)
                        task_str += ' - ' + task_descr["task_begin"]
                    if (task_descr["task_end"] !== undefined)
                        task_str += ' - ' + task_descr["task_end"]
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
                }
            }
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


//save changes button
//$("#create_task_modal_save_button").click(function () {
$(document).on('click', '#create_task_modal_save_button', function () {
    let date_url = get_period(tasklist_settings.type, tasklist_settings.time);
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
      
    $.post(date_url,
    JSON.stringify ({
        "desr"     :                    $("#exampleFormControlTextarea1").val(),
        "priority" :                    $("#task_priority_dropdown_button").text(),
        "traking"  :                    $("#traking_type_dropdown_button").text(),
        "period"   :                    $("#task_period_dropdown_button").text(),
        "is_habit" :                    $("#is_habit").is(':checked'),
        "datetime_start" :              start,
        "datetime_end" :                $("#datetimeinput2").val(),
        "parent_task" :                 $("#parent_task_input").val(),
        "template_intervals" :          {   "active_intervals" :  $("#active_days_input2").val(),
                                            "exclude_selected" :  $("#exclude_selected2").is(':checked'),
                                            "template_counter" :  $("#repeat_counter_form").val() }
    }),
    function(data, status) {
        update_tasks(tasklist_settings, tasklist_settings.type)
    },
    'json');
});

$(document).ready(function() {
    tasklist_settings.type = "Day"
    tasklist_settings.time = new Date()
    update_tasks(tasklist_settings, "Day")
});

$(function() {
    $.contextMenu({
        selector: '#current_tasklist', 
        callback: function(key, options) {
            var m = "clicked: " + key;
            window.console && console.log(m) || alert(m); 
        },
        items: {
            "edit": {name: "Edit", icon: "edit"},
            "delete": {name: "Delete", icon: "delete"},
        }
    });

    $('.context-menu-one').on('click', function(e){
        console.log('clicked', this);
    })    
});

// $("#current_tasklist").on( "click", function( clickE ) {
// $(document).on('click', '#current_tasklist', function (clickE) {
//     alert(clickE.offsetX + ' ' + clickE.offsetY);
//     $.contextMenu( { x: clickE.offsetX, y: clickE.offsetY } );
// });

// $.contextMenu({
//     selector: '#current_tasklist', 
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
