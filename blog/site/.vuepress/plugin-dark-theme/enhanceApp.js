import Darkmode from "darkmode-js";

const darkModeMixin = {
  created() {
    const isRoot = this.$options.isRoot;
    if (!isRoot) return;

    const darkmode = new Darkmode({
      bottom: "32px",
      right: "32px",
      left: "unset",
      time: "0.4s",
      mixColor: "#fff",
      backgroundColor: "#fff",
      buttonColorDark: "#100f2c",
      buttonColorLight: "#fff",
      saveInCookies: true, // Misnomer: whether persisting theme in localStorage is enabled.
      label: "🌗",
      autoMatchOsTheme: true
    });
    darkmode.showWidget();
  }
};

export default ({ Vue }) => {
  Vue.mixin(darkModeMixin);
};
