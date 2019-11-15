import dayjs from "dayjs";

export default ({ Vue }) => {
  Vue.filter("date", function(value, format) {
    return dayjs(value).format("MMMM D, YYYY");
  });

  // TODO
  Vue.prototype.$isAuthenticated = false;
};
