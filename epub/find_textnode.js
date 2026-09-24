function initNodeVariables() {
    window.walker = null;
    window.currNode = null;
}

function initSentenceVariables() {
    window.sentenceNodes = []
    window.sentenceStarts = [];
    window.sentenceCounts = [];
    window.sentences = [];
    window.sentenceHeightOffsets = [];
    window.currSentenceIndex = 0;
}

function createNodesWalker() {
    initNodeVariables();
    let filter = function(node) {
        nodeName = node.tagName.toLowerCase();
        return (nodeName === 'p' || nodeName === 'h1' || 
            nodeName === 'h2' || nodeName === 'h2' || 
            nodeName === 'h3' || nodeName === 'h4' ||
            nodeName === 'h5' || nodeName === 'h6' || 
            nodeName === 'li' || nodeName === 'dt' || 
            nodeName === 'dd' || nodeName === 'blockquote' ||
            nodeName === 'td' || nodeName === 'th' || 
            nodeName === 'span' || nodeName === 'div')
            ? NodeFilter.FILTER_ACCEPT:
            NodeFilter.FILTER_SKIP;
    };
    window.walker = document.createTreeWalker(document.body, 
                                            NodeFilter.SHOW_ELEMENT,
                                            filter, false);
    window.currNode = window.walker.firstChild();
}

function findTextNode(isFirstNode) {
    initSentenceVariables();
    const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    while (window.currNode != null) {
        const rect = window.currNode.getBoundingClientRect();
        const style = window.getComputedStyle(window.currNode);

        // 过滤不可见元素：尺寸为0、display:none、visibility:hidden
        if (rect.width === 0 || rect.height === 0) {
            window.currNode = window.walker.nextSibling();
            continue;
        }
        if (style.display === 'none' || style.visibility === 'hidden') {
            window.currNode = window.walker.nextSibling();
            continue;
        }

        // 判断是否在视口内（任意部分可见就算）
        const isInViewport = (
            rect.top < viewportHeight && rect.bottom > 0 &&
            rect.left < viewportWidth && rect.right > 0
        );

        if (!isInViewport) {
            if (isFirstNode) { 
                window.currNode = window.walker.nextSibling();
                continue;
            } else {
                window.currNode.scrollIntoView({behavior: 'smooth', block: 'start'});
            }
        }
        let offset = 0;
        const sent_len = window.currNode.textContent.length;
        for (child of window.currNode.childNodes) {
            if (child.nodeType === 3) {
                const sv = child.nodeValue.trim();
                const sm = sv.matchAll(/.+?([\\.。]|$)/gu);
                if (sm != null) {
                    for (s of sm) {
                        window.sentenceNodes = window.sentenceNodes.concat(child);
                        window.sentenceStarts = window.sentenceStarts.concat(s.index);
                        window.sentenceCounts = window.sentenceCounts.concat(s[0].length);
                        window.sentences = window.sentences.concat(s[0]);
                        window.sentenceHeightOffsets = 
                            window.sentenceHeightOffsets.concat(offset)
                        offset += s[0].length / sent_len;
                    }
                }
            } else {
                const sv = child.textContent;
                if (sv != null) {
                    window.sentenceNodes = window.sentenceNodes.concat(child);
                    window.sentenceStarts = window.sentenceStarts.concat(0);
                    window.sentenceCounts = window.sentenceCounts.concat(child.childNodes.length);
                    window.sentences = window.sentences.concat(sv);
                    window.sentenceHeightOffsets = 
                        window.sentenceHeightOffsets.concat(offset);
                    offset += sv.length / sent_len;
                }
            }
        }
        if (window.sentenceNodes != null) {
            let ind = window.currSentenceIndex;
            do {
                let top = rect.top + 
                    window.sentenceHeightOffsets[ind] * rect.height;
                /*console.log("ind, curr_index, node.len: ", 
                    ind, window.currSentenceIndex, 
                    window.sentenceNodes.length);
                console.log("rect.top, rect.height, sent_offset:",
                    rect.top, rect.height,
                    window.sentenceHeightOffsets[ind]);
                console.log(window.sentences[ind]);*/
                if (top >= 0) break;
                ind ++;
            } while (ind < window.sentenceNodes.length);
            if (ind < window.sentenceNodes.length)
                window.currSentenceIndex = ind;
            selectCurrentSentence();
            const return_val = {href:window.currNode.id, 
                sentence:window.sentences[window.currSentenceIndex]};
            return JSON.stringify(return_val);
        }
        window.currNode = window.walker.nextSibling();
    }
    return JSON.stringify({href:"",sentence:""}); 
}

function selectCurrentSentence() {
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    const rect = window.sentenceNodes[window.currSentenceIndex].nodeType === 3 ?
        window.currNode.getBoundingClientRect() :
        window.sentenceNodes[window.currSentenceIndex].getBoundingClientRect();
    const sent_top = rect.top + 
        window.sentenceHeightOffsets[window.currSentenceIndex] * rect.height;
    if (sent_top > viewportHeight * 0.9)
        window.scrollBy(0, sent_top * 0.9);
    else if (sent_top < 0)
        window.scrollBy(0, sent_top);
    const range = document.createRange();
    range.setStart(window.sentenceNodes[window.currSentenceIndex], 
        window.sentenceStarts[window.currSentenceIndex]);
    range.setEnd(window.sentenceNodes[window.currSentenceIndex], 
        window.sentenceStarts[window.currSentenceIndex] + 
        window.sentenceCounts[window.currSentenceIndex]);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
}

function retrieveFirstSentence() {
    createNodesWalker();
    return findTextNode(true);
}

function retrieveNextSentence() {
    window.currSentenceIndex++;
    if (window.currSentenceIndex < window.sentenceNodes.length) {
        selectCurrentSentence();
        const return_val = {href:"",
            sentence:window.sentences[window.currSentenceIndex]
        }
        return JSON.stringify(return_val);
    } else {
        window.currNode = window.walker.nextSibling();
        return findTextNode(false);
    }
}
