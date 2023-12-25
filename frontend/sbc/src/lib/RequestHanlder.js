import axios from "axios";
import {PORT, SERVER_URL} from "./constants/Server.js";

export const requestGenerator = (httpmethod, endpoint, params, header, body) => {
    return axios({
        method: httpmethod,
        url: endpoint,
        params: params,
        header: header,
        data: body,
        validateStatus: (status) => {
            return status >= 200 && status < 300;
        },
        proxy: {
            host: SERVER_URL,
            port: PORT
        }
    })
}