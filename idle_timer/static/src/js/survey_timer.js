/** @odoo-module **/

//import { deserializeDateTime } from "@web/core/l10n/dates";
//import publicWidget from "@web/legacy/js/public/public_widget";
//const { DateTime } = luxon;
//
//
//SurveyFormWidget.include({
//    /**
//     * @override
//     */
//
//    init: function (parent, params) {
//        this._super.apply(this, arguments).then(function(){
//        return this._super.apply(this, arguments).then(function() {
//        this.idleTimeMinutes = params.idleTime;
//        this.inactivityTime = this.idleTimeMinutes * 60 * 1000; // Convert minutes to milliseconds
//        this.inactivityTimer = null;
//        this.lastActivity = Date.now();
//        this.initEventListeners();
//
//            },
//        });
//    }
//    initEventListeners: function () {
//        document.addEventListener('mousemove', this.resetInactivityTimer.bind(this));
//        document.addEventListener('keypress', this.resetInactivityTimer.bind(this));
//        this.startInactivityTimer();
//    },
//
//    resetInactivityTimer: function () {
//        this.lastActivity = Date.now();
//        clearTimeout(this.inactivityTimer);
//        this.startInactivityTimer();
//    },
//
//    startInactivityTimer: function () {
//        this.inactivityTimer = setTimeout(() => {
//            const currentTime = Date.now();
//            if (currentTime - this.lastActivity >= this.inactivityTime) {
//                this.trigger_up('time_up'); // Trigger an event when time is up
//            }
//        }, this.inactivityTime);
//    },
//
//    willUnmount: function () {
//        clearTimeout(this.inactivityTimer);
//        document.removeEventListener('mousemove', this.resetInactivityTimer);
//        document.removeEventListener('keypress', this.resetInactivityTimer);
//        document.removeEventListener('mouseup'),this.
//    },
//}
//});
//
//
//export default publicWidget.registry.IdleSurveyTimerWidget;



//_____________________________________________________________________________


///** @odoo-module **/
//
//import publicWidget from "@web/legacy/js/public/public_widget";
//import { useService } from "@web/core/utils/hooks";
//import SurveyFormWidget from '@survey/js/survey_form';
//
//
////publicWidget.registry.IdleSurveyTimerWidget = publicWidget.Widget.extend({
////    selector: '.o_survey_form',
////    events:{
////        'mousemove .o_survey_form' : '_onMouseMove',
////        'keypress .o_survey_form' : '_onKeypress',
////    },
//
//SurveyFormWidget.include({
//    init(){
//        this._super(...arguments);
//        this.orm = this.bindService("orm");
//    },
//
//    start: async function(options){
//        console.log('ssssss')
//        this.result = await this.orm.call('ir.config_parameter','get_param',[this.idle_time]);
//        console.log('Idle time =',this.result)
////        this.idleTime = null;
//    },
//
//    initIdleTimer: function (){
//        var idleTime = parseInt(this.quiz_idle_time) || 60;
//        var timeoutDuration = parseInt(this.quiz_timeout_duration)|| 120;
//        idleSeconds = 0;
//        var self = this;
//
//        function resetTimer() {
//            idleSeconds = 0;
//        $(document).on('mousemove keydown',resetTimer);
//        var interval = setInterval(function (){
//            idleSeconds ++;
//            $(document).on('mousemove keydown',resetTimer);
//            if (idleSeconds >= idleTime){
//                idleSeconds = 0;
//                clearInterval(interval);
//                self.startTimeout(timeoutDuration);
//                }
//        },1000);
//        }
//    },
//
//    moveToNextPage : function (){
//        var nextButton = document.querySelector('button[type="submit"]');
//        if(nextButton){
//        nextButton.click();
//        this.initIdleTimer();
//        }
//    }
//});

