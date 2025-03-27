import MainComponent from "../../components/MainComponent.vue";
import DetailContent from "../../components/details/DetailContent.vue";
import About from "../../components/footer/about/About.vue";
import Disclaimer from "../../components/footer/disclaimer/Disclaimer.vue";
import Privacy from "../../components/footer/privacy/Privacy.vue";
import YtTutorials from "../../components/footer/yt_tutorials/YoutubeTutorials.vue";

export const routes = [
	{ path: '/sbc-shap', component: MainComponent },
	{ path: '/yt-tutorials', component: YtTutorials },
	{ path: '/sbc-shap/about', component: About },
	{ path: '/sbc-shap/disclaimer', component: Disclaimer },
	{ path: '/sbc-shap/details/:id', component: DetailContent},
	{ path: '/sbc-shap/data-privacy', component: Privacy}
]
