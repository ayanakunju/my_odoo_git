/** @odoo-module **/

import { deserializeDateTime } from "@web/core/l10n/dates";
import SurveyFormWidget from '@survey/js/survey_form';
const { DateTime } = luxon;
import { jsonrpc } from "@web/core/network/rpc_service";


SurveyFormWidget.include({
    /**
     * @override
     */
    start: function(){
        console.log('ssss sssss ssss')
        var self = this;
        return this._super.apply(this, arguments).then(function() {
            self.idleTimeout();
            jsonrpc('/get_idle_time/timer').then(function (data) {
                if (data) {
                    self.minutes = data;
                    console.log('dataaaaaaaaaaaa',self.minutes)
                    self.idleTimeout();
                }
            });
        });
    },

    idleTimeout: function(){
        console.log('qqqqqqqqqqqqqqqqq')
        var idlestate;
        var self = this
        window.onload = resetTimer;
        window.onmousemove = resetTimer;
        window.onmousedown = resetTimer;    // catches touchscreen presses as well
        window.ontouchstart = resetTimer;   // catches touchscreen swipes as well
        window.ontouchmove = resetTimer;    // required by some devices
        window.onclick = resetTimer;        // catches touchpad clicks as well
        window.onkeydown = resetTimer;
        window.addEventListener('scroll', resetTimer, true);

        function idleTimer() {
            console.log('tttttttttttttttttt')
            self.time = self.minutes.idle_time
            self.timeStamp = new Date().getTime() + self.time * 60 * 1000;
            self.show_idle_time();
            self.surveyTimerInterval = setInterval(self.show_idle_time.bind(self), 1000);
        }

        function resetTimer() {
            console.log('timer')
            clearTimeout(idlestate);
            clearInterval(self.surveyTimerInterval);
            idlestate = setTimeout(idleTimer, self.minutes.idle_seconds * 1000);  // time is in milliseconds
        }

    },

    show_idle_time: function(){
        var self =this;
        var timeLeft = (this.timeStamp - new Date().getTime())/1000;
        console.log("timeleft", timeLeft, self.$('.o_survey_timer_container'))

        if (timeLeft >= 0){
        self.$('.o_survey_timer_container').show();
            var minutes = parseInt(timeLeft / 60);
            var seconds = Math.floor(timeLeft - (minutes * 60));
            var $idleTime = self.$('.o_survey_timer_container');
            $idleTime.text(minutes+':'+seconds)

            console.log(minutes+':'+seconds,'eeeeeeeeeeeeeeeeeee')

        } else {
            console.log('time upppppppppppp')
            self.$('.o_survey_timer_container').text('');
            clearInterval(self.surveyTimerInterval);
            self.idleTimeout()
              const options = {}
              options.initTime = true;
              var skipValidation = true
              this._submitForm(options)
        }
    },
});
