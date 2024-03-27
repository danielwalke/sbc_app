import MainComponent from "../components/MainComponent.vue";
import DetailContent from "../components/details/DetailContent.vue";
import About from "../components/about/About.vue";
import Disclaimer from "../components/disclaimer/Disclaimer.vue";

export const routes = [
	{ path: '/frontend', component: MainComponent },
	{ path: '/frontend/about', component: About },
	{ path: '/frontend/disclaimer', component: Disclaimer },
	{ path: '/frontend/details/:id', component: DetailContent}
]
