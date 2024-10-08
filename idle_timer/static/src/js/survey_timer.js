/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillUnmount, useState, useEffect} from "@odoo/owl";

const { Component, mount } = owl;
const { useState, useEffect } = owl.hooks;

    class QuizTimer extends Component {
        setup() {
            this.state = useState({ isIdle: false });
            this.idleTime = 0;
            this.timerInterval = null;
            this.redirectTime = this.props.redirectTime * 1000; // Convert to milliseconds
            this.startIdleTimer();
        }

        startIdleTimer() {
            // Reset idle time on user activity
            document.addEventListener('mousemove', this.resetIdleTime.bind(this));
            document.addEventListener('keypress', this.resetIdleTime.bind(this));

            // Start the idle timer
            this.timerInterval = setInterval(() => {
                this.idleTime += 1000; // Increment idle time by 1 second

                const idleLimit = this.props.idleTime * 1000; // Convert to milliseconds
                if (this.idleTime >= idleLimit) {
                    this.state.isIdle = true;
                    this.redirectToNextPage();
                }
            }, 1000);
        }

        resetIdleTime() {
            this.idleTime = 0; // Reset idle time
            this.state.isIdle = false; // Reset idle state
        }

        async redirectToNextPage() {
            // Delay for redirect time before navigating
            await this.delayRedirect();
            window.location.href = '/next_quiz_page'; // Adjust this URL as needed
        }

        delayRedirect() {
            return new Promise(resolve => setTimeout(resolve, this.redirectTime));
        }

        onWillUnmount() {
            clearInterval(this.timerInterval);
            document.removeEventListener('mousemove', this.resetIdleTime.bind(this));
            document.removeEventListener('keypress', this.resetIdleTime.bind(this));
        }

        static template = 'idle_timer.QuizTimer';
    }

    // Mount the component in the appropriate HTML container
    mount(QuizTimer, document.getElementById('quiz_timer_container')); // Ensure this ID is present in your HTML
});
