import TableInput from "../components/TableInput.vue";
import DetailContent from "../components/details/DetailContent.vue";
import About from "../components/about/About.vue";
import Disclaimer from "../components/disclaimer/Disclaimer.vue";

export const routes = [
	{ path: '/sbc_frontend', component: TableInput },
	{ path: '/about', component: About },
	{ path: '/disclaimer', component: Disclaimer },
	{ path: '/details/:id', component: DetailContent}
]
