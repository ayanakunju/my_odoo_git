/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import {Dropdown} from '@web/core/dropdown/dropdown';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import { useState} from "@odoo/owl";

class SystrayIcon extends Component {
 setup() {
   super.setup(...arguments);
   this.action = useService("action");
    this.state = useState({
      weatherData: null,
      temp : null,
      date: new Date().toDateString(),
      iconUrl: null,
      iconCode: null
    });
 }
 async _onClick() {
   const response = await fetch('https://api.openweathermap.org/data/2.5/weather?lat=11.25&lon=75.78&appid=4229b2f577176988d758e61ecb837801')
  .then(response => response.json())
  .then (data => this.state.weatherData = data)
  .then (data => this.state.temp = (data.main.temp/10).toFixed(2))
  .then (data => this.state.iconCode = this.state.weatherData.weather[0].icon)
  .then(data => this.state.iconUrl = "http://openweathermap.org/img/w/" + this.state.iconCode + ".png")

   console.log(this.state.weatherData)

   }
   }

SystrayIcon.template = "weather_systray";
SystrayIcon.components = {Dropdown,DropdownItem};
export const systrayItem = {Component: SystrayIcon,};
registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 1 });
