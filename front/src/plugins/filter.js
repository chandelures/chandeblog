"use strict";

import Vue from "vue";

Vue.filter("formatDate", (dateStr) => {
  var date = new Date(dateStr);
  var monthNames = new Array(
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Spt",
    "Oct",
    "Nov",
    "Dec"
  );
  var year = date.getFullYear();
  var month = date.getMonth();
  var day = date.getDate();
  return monthNames[month] + " " + day + ", " + year;
});

export default Vue;
