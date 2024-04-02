import MainComponent from "../components/MainComponent.vue";
import DetailContent from "../components/details/DetailContent.vue";
import About from "../components/about/About.vue";
import Disclaimer from "../components/disclaimer/Disclaimer.vue";

export const routes = [
	{ path: '/sbc_frontend', component: MainComponent },
	{ path: '/sbc_frontend/about', component: About },
	{ path: '/sbc_frontend/disclaimer', component: Disclaimer },
	{ path: '/sbc_frontend/details/:id', component: DetailContent}
]
