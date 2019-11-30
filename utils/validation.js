function(newDoc, oldDoc, userCtx) {
    if (~userCtx.roles.indexOf('_admin')) {
        log('Server admin change on document: ' + newDoc._id);
    } else if (userCtx.name === 'device_' + newDoc.device) {
        if (!oldDoc || newDoc.device === oldDoc.device) {
            log('Device ' + newDoc.device + ' change on document: ' + newDoc._id);
        } else {
            throw {
                'forbidden': 'Device id cannot be changed.'
            }
        }
    } else {
        throw {
            'unauthorized': 'guests cannot write documents.'
        }
    }
}
