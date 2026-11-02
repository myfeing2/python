document.addEventListener('click', function (event) {
    //console.log(event.target); // 点击哪个元素，这里就输出哪个
    createNodesWalker();
    window.currNode = window.walker.firstChild();
    while (window.currNode != null) {
        if (window.currNode.contains(event.target)) {
            //console.log("Clicked node: ", window.currNode);
            let first_sentence = findTextNode(false);
            window.bridge.start_playback(first_sentence);
            break;
        }
        window.currNode = window.walker.nextSibling();
    }
    return 
});

function initWebChannel() {
    let script = document.createElement("script");
    script.src = "qrc:///qtwebchannel/qwebchannel.js";
    script.onload = function() {
        //console.log('✅ qwebchannel.js脚本加载成功');
        // 这里可以安全调用脚本里的函数
        if(typeof QWebChannel === 'undefined') {
            console.error('❌ QWebChannel 未定义');
            return;
        }
        if(typeof qt === 'undefined' || !qt.webChannelTransport) {
            console.error('❌ qt 或 qt.webChannelTransport 未定义');
            return;
        }
        new QWebChannel(qt.webChannelTransport, function(channel) {
            window.bridge = channel.objects.bridge;  // 这里才拿到对象
            console.log('bridge初始化成功', window.bridge);
            observeTextNodeMovement();
        });
    };
    script.onerror = function() {
        console.log('❌ 脚本加载失败');
    };
    document.body.appendChild(script);
}

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
        const style = window.getComputedStyle(node);
        if (style.display === 'none' || style.visibility === 'hidden') {
          return NodeFilter.FILTER_REJECT; // 跳过整个子树
        }
        if (node.offsetWidth === 0 || node.offsetHeight === 0) {
          return NodeFilter.FILTER_REJECT; // 跳过整个子树
        }
        if (node.textContent.trim() === '') {
            return NodeFilter.FILTER_REJECT; // 跳过整个子树
        }
        return (nodeName === 'p' || nodeName === 'h1' || 
            nodeName === 'h2' || nodeName === 'h2' || 
            nodeName === 'h3' || nodeName === 'h4' ||
            nodeName === 'h5' || nodeName === 'h6' || 
            nodeName === 'li' || nodeName === 'dt' || 
            nodeName === 'dd' || nodeName === 'blockquote' ||
            nodeName === 'td' || nodeName === 'th' || 
            nodeName === 'span')
            ? NodeFilter.FILTER_ACCEPT:
            NodeFilter.FILTER_SKIP;
    };
    window.walker = document.createTreeWalker(document.body, 
                                            NodeFilter.SHOW_ELEMENT,
                                            filter, false);
}

function findTextNode(isFirstEntry) {
    initSentenceVariables();
    const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    while (window.currNode != null) {
        const rect = window.currNode.getBoundingClientRect();
        if (isFirstEntry) {
            const style = window.getComputedStyle(window.currNode);

            // 过滤不可见元素：尺寸为0、display:none、visibility:hidden
            /*if (rect.width === 0 || rect.height === 0) {
                window.currNode = window.walker.nextSibling();
                continue;
            }*/
            /*if (style.display === 'none' || style.visibility === 'hidden') {
                window.currNode = window.walker.nextSibling();
                continue;
            }*/

            // 判断是否在视口内（任意部分可见就算）
            const isInViewport = (
                rect.top < viewportHeight && rect.bottom > 0 &&
                rect.left < viewportWidth && rect.right > 0
            );
            console.log(rect.top, window.currNode.textContent);
            if (!isInViewport) {
                window.currNode = window.walker.nextSibling();
                continue;
            }
        }
        
        let offset = 0;
        const sent_len = window.currNode.textContent.length;
        for (child of window.currNode.childNodes) {
            //console.log("child nodeType: ", child.nodeType, child.nodeName);
            //console.log("child node: ", child);
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
                //console.log("child text: ", sv);
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
            if (isFirstEntry) {
                let ind = window.currSentenceIndex;
                do {
                    let top = rect.top + 
                        window.sentenceHeightOffsets[ind] * rect.height;
                    //console.log("ind, rect.top, sent_offset:",
                    //    ind, rect.top, window.sentenceHeightOffsets[ind]);
                    //console.log(window.sentences[ind]);
                    if (top >= 0) break;
                    ind ++;
                } while (ind < window.sentenceNodes.length);
                if (ind < window.sentenceNodes.length)
                    window.currSentenceIndex = ind;
                //console.log("ind, sent_ind: ", ind, window.currSentenceIndex);
                scrollToSentence();
            }
            selectSentence();
            const return_val = {href:window.currNode.id, 
                sentence:window.sentences[window.currSentenceIndex]};
            return JSON.stringify(return_val);
        }
        window.currNode = window.walker.nextSibling();
    }
    return JSON.stringify({href:"",sentence:""}); 
}

function selectSentence() {
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

function isInViewport() {
    const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    const rect = window.sentenceNodes[window.currSentenceIndex].nodeType === 3 ?
        window.currNode.getBoundingClientRect() :
        window.sentenceNodes[window.currSentenceIndex].getBoundingClientRect();
    const sent_top = rect.top + 
        window.sentenceHeightOffsets[window.currSentenceIndex] * rect.height;
    return (
        sent_top > 0 && sent_top < viewportHeight &&
        rect.left < viewportWidth && rect.right > 0
    );
}

function scrollToSentence() {
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
    //console.log("sent_top: ", sent_top);
}

function retrieveFirstSentence() {
    createNodesWalker();
    window.currNode = window.walker.firstChild();
    return findTextNode(true);
}

function retrieveNextSentence() {
    isNeedScroll = isInViewport();
    window.currSentenceIndex++;
    if (window.currSentenceIndex < window.sentenceNodes.length) {
        selectSentence();
        if (isNeedScroll) scrollToSentence();
        const return_val = {href:"",
            sentence:window.sentences[window.currSentenceIndex]
        }
        return JSON.stringify(return_val);
    } else {
        window.currNode = window.walker.nextSibling();
        next_sentence = findTextNode(false);
        if (isNeedScroll) scrollToSentence();
        return next_sentence;
    }
}

function scrollToText(escaped) {
    // 在页面所有元素中查找包含目标文本的元素
    const walker = document.createTreeWalker(
        document.body, NodeFilter.SHOW_ELEMENT, {
            acceptNode(node) {
                return node.id === escaped
                    ? NodeFilter.FILTER_ACCEPT
                    : NodeFilter.FILTER_SKIP;
            }
        }
    );
    const node = walker.nextNode();
    if (node) {
        //console.log(node.textContent);
        node.scrollIntoView({behavior: 'auto', block: 'start'});
    }
}

function observeTextNodeMovement() {
    const io = new IntersectionObserver((entries, ob) => {
        entries.forEach(en => {
            if (en.isIntersecting && en.intersectionRatio > 0) {
                window.bridge.add_visible(en.target.id);
                //console.log("Node visible: ", en.target.id);
            } else if (!en.isIntersecting || en.intersectionRatio === 0) {
                //console.log("Node not visible: ", en.target.id);
                //console.log("  rootBounds: ", en.rootBounds.top, en.rootBounds.bottom);
                //console.log("  boundingClientRect: ", en.boundingClientRect.top, en.boundingClientRect.bottom);
                if (en.boundingClientRect.bottom >= en.rootBounds.bottom) {
                    window.bridge.scroll_up(en.target.id);
                    //console.log("  Node scroll_up: ", en.target.id);
                    return;
                } 
                if (en.boundingClientRect.top <= en.rootBounds.top) {
                    window.bridge.scroll_down(en.target.id);
                    //console.log("  Node scroll_down: ", en.target.id);
                    return;
                }
            }
        });
    }, { threshold: 1 });

    document.querySelectorAll('p[id]:not([id=""]), \
        h1[id]:not([id=""]), h2[id]:not([id=""]), \
        h3[id]:not([id=""]), h4[id]:not([id=""]), \
        h5[id]:not([id=""]), h6[id]:not([id=""]), \
        li[id]:not([id=""]), dt[id]:not([id=""]), \
        dd[id]:not([id=""]), blockquote[id]:not([id=""]), \
        td[id]:not([id=""]), th[id]:not([id=""]), \
        span[id]:not([id=""])').forEach(tn => io.observe(tn));
}
