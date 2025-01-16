import MainComponent from "../../components/MainComponent.vue";
import DetailContent from "../../components/details/DetailContent.vue";
import About from "../../components/footer/about/About.vue";
import Disclaimer from "../../components/footer/disclaimer/Disclaimer.vue";

export const routes = [
	{ path: '/sbc', component: MainComponent },
	{ path: '/sbc/about', component: About },
	{ path: '/sbc/disclaimer', component: Disclaimer },
	{ path: '/sbc/details/:id', component: DetailContent}
]
