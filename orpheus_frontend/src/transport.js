import {GET_CONTENT_URL, SEARCH_URL} from "./constrants"

export function searchByQuery(query) {
    return fetch(`${SEARCH_URL}?${new URLSearchParams({ text: query })}`)
        .then((res) => res.json())
        .then((data) => data.items);
}

export function getContent(id, index) {
    return fetch(`${GET_CONTENT_URL}?${new URLSearchParams({ id: id, index: index })}`)
        .then((res) => res.json())
}
