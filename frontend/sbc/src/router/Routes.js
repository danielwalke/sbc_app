import TableInput from "../components/TableInput.vue";
import DetailContent from "../components/details/DetailContent.vue";
import About from "../components/about/About.vue";

export const routes = [
	{ path: '/', component: TableInput },
	{ path: '/about', component: About },
	{ path: '/details/:id', component: DetailContent}
]
