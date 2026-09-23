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
            selectCurrentSentence();
            return window.sentences[window.currSentenceIndex];
        }
        window.currNode = window.walker.nextSibling();
    }
    return ""; 
}

function selectCurrentSentence() {
    const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    const rect = window.sentenceNodes[window.currSentenceIndex].nodeType === 3 ?
        window.currNode.getBoundingClientRect():
        window.sentenceNodes[window.currSentenceIndex].getBoundingClientRect(); 
    const isInViewport = (
        rect.top < viewportHeight && rect.bottom > 0 &&
        rect.left < viewportWidth && rect.right > 0
    );
   if (!isInViewport) {
        window.sentenceNodes[window.currSentenceIndex].scrollIntoView({behavior: 'smooth', block: 'start'});
    } else {
        offset = window.sentenceHeightOffsets[window.currSentenceIndex] * 
            rect.height;
        sent_top = rect.top + offset
        if (sent_top  > viewportHeight * 0.9) {
            window.scrollBy(0, sent_top * 0.9);
        }
    }
    range = document.createRange();
    range.setStart(window.sentenceNodes[window.currSentenceIndex], 
        window.sentenceStarts[window.currSentenceIndex]);
    range.setEnd(window.sentenceNodes[window.currSentenceIndex], 
        window.sentenceStarts[window.currSentenceIndex] + 
        window.sentenceCounts[window.currSentenceIndex]);
    selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
}

function retrieveFirstSentence() {
    window.currNode = window.walker.firstChild();
    return findTextNode(true);
}

function retrieveNextSentence() {
    window.currSentenceIndex++;
    if (window.currSentenceIndex < window.sentences.length) {
        selectCurrentSentence();
        return window.sentences[window.currSentenceIndex];
    } else {
        window.currNode = window.walker.nextSibling();
        return findTextNode(false);
    }
}
