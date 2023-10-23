import { TASK_STATUSES } from '../config/statuses';

export const STATUSES = {
    PROPOSED: 0,
    INPROGRESS: 1,
    BLOCKED: 2,
    DONE: 3,
    NOT_INTERESTED: 4,
}

export const STATUS_TEXT = {
    0: "nouveau",
    1: "en cours",
    2: "en attente",
    3: "faite",
    4: "non applicable",
}

export function statusText(status) {
    return STATUS_TEXT[status];
}

export function isStatus(task, status) {
    return task.status === status
}

export function isArchivedStatus(status) {
    return status === STATUSES.DONE
        || status === STATUSES.NOT_INTERESTED
}

export function isStatusUpdate(followup) {
    return isArchivedStatus(followup.status) || followup.comment === "";
}

export function truncate(input, size = 30) {
    return input.length > size ? `${input.substring(0, size)}...` : input;
}
